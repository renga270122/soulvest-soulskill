import 'dart:convert';

import 'package:http/http.dart' as http;

class ApiClient {
  ApiClient({http.Client? client}) : _client = client ?? http.Client();

  final http.Client _client;

  static const String _configuredBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://10.0.2.2:8000',
  );

  String get baseUrl => _configuredBaseUrl.replaceFirst(RegExp(r'/+$'), '');

  Future<String> improveProfessionalSummary({
    required String summary,
    required String role,
  }) async {
    final uri = Uri.parse('$baseUrl/api/ai/improve-summary');
    final response = await _client
        .post(
          uri,
          headers: const {'Content-Type': 'application/json'},
          body: jsonEncode({'summary': summary, 'role': role}),
        )
        .timeout(const Duration(seconds: 35));

    Map<String, dynamic> payload;
    try {
      payload = jsonDecode(response.body) as Map<String, dynamic>;
    } on FormatException {
      throw const ApiException('The server returned an unreadable response.');
    }

    if (response.statusCode < 200 || response.statusCode >= 300) {
      final detail = payload['detail']?.toString();
      throw ApiException(
        detail?.isNotEmpty == true
            ? detail!
            : 'AI service request failed (${response.statusCode}).',
      );
    }

    final improved = payload['improved']?.toString().trim() ?? '';
    if (improved.isEmpty) {
      throw const ApiException('The AI service did not return improved content.');
    }
    return improved;
  }

  void close() => _client.close();
}

class ApiException implements Exception {
  const ApiException(this.message);

  final String message;

  @override
  String toString() => message;
}
