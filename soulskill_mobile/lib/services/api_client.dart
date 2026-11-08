import 'dart:convert';
import 'dart:typed_data';

import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:http/http.dart' as http;

import '../models/resume_model.dart';

class ApiClient {
  ApiClient({http.Client? client}) : _client = client ?? http.Client();

  final http.Client _client;

  static const String _configuredBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
  );

  String get baseUrl {
    final configured = _configuredBaseUrl.trim();
    if (configured.isNotEmpty) {
      return configured.replaceFirst(RegExp(r'/+$'), '');
    }
    return kIsWeb ? Uri.base.origin : 'http://10.0.2.2:8000';
  }

  Future<String> improveProfessionalSummary({
    required String summary,
    required String role,
  }) async {
    final uri = Uri.parse(baseUrl + '/api/ai/improve-summary');
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
    } on TypeError {
      throw const ApiException('The server returned an unexpected response.');
    }

    if (response.statusCode < 200 || response.statusCode >= 300) {
      final detail = payload['detail']?.toString();
      throw ApiException(
        detail?.isNotEmpty == true
            ? detail!
            : 'AI service request failed (' + response.statusCode.toString() + ').',
      );
    }

    final improved = payload['improved']?.toString().trim() ?? '';
    if (improved.isEmpty) {
      throw const ApiException('The AI service did not return improved content.');
    }
    return improved;
  }

  Future<Map<String, dynamic>> analyzeResumeForJob({
    required ResumeModel resume,
    required String jobDescription,
    required String targetRole,
  }) async {
    final response = await _client
        .post(
          Uri.parse(baseUrl + '/api/resume/job-fit'),
          headers: const {'Content-Type': 'application/json'},
          body: jsonEncode({
            'resume': resume.toApiJson(),
            'job_description': jobDescription,
            'target_role': targetRole,
          }),
        )
        .timeout(const Duration(seconds: 35));
    return _decodeMap(response);
  }

  Future<Map<String, dynamic>> parseResumeFile({
    required Uint8List bytes,
    required String fileName,
  }) async {
    final request = http.MultipartRequest(
      'POST',
      Uri.parse(baseUrl + '/api/resume/parse'),
    );
    request.files.add(
      http.MultipartFile.fromBytes('file', bytes, filename: fileName),
    );
    final streamed = await _client.send(request).timeout(const Duration(seconds: 60));
    final response = await http.Response.fromStream(streamed);
    return _decodeMap(response);
  }

  Map<String, dynamic> _decodeMap(http.Response response) {
    Map<String, dynamic> payload;
    try {
      payload = jsonDecode(response.body) as Map<String, dynamic>;
    } on FormatException {
      throw const ApiException('The server returned an unreadable response.');
    } on TypeError {
      throw const ApiException('The server returned an unexpected response.');
    }

    if (response.statusCode < 200 || response.statusCode >= 300) {
      final detail = payload['detail']?.toString();
      throw ApiException(
        detail?.isNotEmpty == true
            ? detail!
            : 'The request failed (' + response.statusCode.toString() + ').',
      );
    }
    return payload;
  }

  void close() => _client.close();
}

class ApiException implements Exception {
  const ApiException(this.message);

  final String message;

  @override
  String toString() => message;
}
