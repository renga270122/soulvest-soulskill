import 'package:flutter_test/flutter_test.dart';
import 'package:soulskill_mobile/services/api_client.dart';

void main() {
  group('resolveApiBaseUrl', () {
    test('uses localhost for browser development by default', () {
      expect(
        resolveApiBaseUrl(isWeb: true),
        'http://127.0.0.1:8000',
      );
    });

    test('uses Android emulator host for native development by default', () {
      expect(
        resolveApiBaseUrl(isWeb: false),
        'http://10.0.2.2:8000',
      );
    });

    test('uses an explicit configured URL before platform defaults', () {
      expect(
        resolveApiBaseUrl(
          isWeb: true,
          configuredBaseUrl: 'https://api.soulskill.example/',
        ),
        'https://api.soulskill.example',
      );
    });

    test('uses constructor override before compile-time configuration', () {
      expect(
        resolveApiBaseUrl(
          isWeb: true,
          configuredBaseUrl: 'https://configured.example',
          overrideBaseUrl: 'http://localhost:9000/',
        ),
        'http://localhost:9000',
      );
    });

    test('trims whitespace and trailing slashes', () {
      expect(
        resolveApiBaseUrl(
          isWeb: true,
          configuredBaseUrl: ' https://api.example.com/// ',
        ),
        'https://api.example.com',
      );
    });
  });
}
