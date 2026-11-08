import 'dart:async';
import 'dart:convert';

import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:http/http.dart' as http;

class ApiClient {
  ApiClient({http.Client? client, String? baseUrl})
      : _client = client ?? http.Client(),
        _baseUrlOverride = baseUrl;

  final http.Client _client;
  final String? _baseUrlOverride;

  static const String _configuredBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: '',
  );

  String get baseUrl => resolveApiBaseUrl(
        isWeb: kIsWeb,
        configuredBaseUrl: _configuredBaseUrl,
        overrideBaseUrl: _baseUrlOverride,
      );

  Future<String> improveProfessionalSummary({
    required String summary,
    required String role,
  }) async {
    final uri = Uri.parse('$baseUrl/api/ai/improve-summary');

    late final http.Response response;
    try {
      response = await _client
          .post(
            uri,
            headers: const {'Content-Type': 'application/json'},
            body: jsonEncode({'summary': summary, 'role': role}),
          )
          .timeout(const Duration(seconds: 35));
    } on http.ClientException {
      throw ApiException(
        'Cannot reach the SoulSkill API at $baseUrl. Check that the backend '
        'is running, the API URL is correct, and the browser origin is allowed.',
      );
    } on TimeoutException {
      throw const ApiException(
        'The AI service took too long to respond. Please try again.',
      );
    }

    Map<String, dynamic> payload;
    try {
      final decoded = jsonDecode(response.body);
      if (decoded is! Map<String, dynamic>) {
        throw const FormatException('Expected a JSON object.');
      }
      payload = decoded;
    } on FormatException {
      throw const ApiException('The server returned an unreadable response.');
    }

    if (response.statusCode < 200 || response.statusCode >= 300) {
      final detail = payload['detail']?.toString();
      final fallback = 'AI service request failed (' +
          response.statusCode.toString() +
          ').';
      throw ApiException(detail?.isNotEmpty == true ? detail! : fallback);
    }

    final improved = payload['improved']?.toString().trim() ?? '';
    if (improved.isEmpty) {
      throw const ApiException(
        'The AI service did not return improved content.',
      );
    }
    return improved;
  }

  void close() => _client.close();
}

/// Resolves the API origin for the current platform.
///
/// Priority:
/// 1. Explicit constructor override (useful for tests/integration).
/// 2. API_BASE_URL compile-time define (staging/production/physical device).
/// 3. Local development fallback for Chrome or Android emulator.
///
/// A physical Android device should use the computer's LAN IP via
/// --dart-define=API_BASE_URL=http://<computer-lan-ip>:8000.
/// Production builds must provide an HTTPS API_BASE_URL.
String resolveApiBaseUrl({
  required bool isWeb,
  String configuredBaseUrl = '',
  String? overrideBaseUrl,
}) {
  final override = overrideBaseUrl?.trim() ?? '';
  final configured = configuredBaseUrl.trim();
  final selected = override.isNotEmpty
      ? override
      : configured.isNotEmpty
          ? configured
          : isWeb
              ? 'http://127.0.0.1:8000'
              : 'http://10.0.2.2:8000';

  return selected.replaceFirst(RegExp(r'/+$'), '');
}

class ApiException implements Exception {
  const ApiException(this.message);

  final String message;

  @override
  String toString() => message;
}
