import 'package:flutter/material.dart';

class SoulSkillTheme {
  static const Color ink = Color(0xFF20183D);
  static const Color muted = Color(0xFF706A83);
  static const Color canvas = Color(0xFFF7F5FC);
  static const Color violet = Color(0xFF6842D8);
  static const Color lavender = Color(0xFF9B7AF5);
  static const Color border = Color(0xFFEAE6F3);

  static ThemeData get light {
    final scheme = ColorScheme.fromSeed(
      seedColor: violet,
      brightness: Brightness.light,
    ).copyWith(
      primary: violet,
      secondary: lavender,
      surface: Colors.white,
    );

    return ThemeData(
      useMaterial3: true,
      colorScheme: scheme,
      scaffoldBackgroundColor: canvas,
      appBarTheme: const AppBarTheme(
        backgroundColor: Colors.white,
        foregroundColor: ink,
        elevation: 0,
        centerTitle: false,
        titleTextStyle: TextStyle(color: ink, fontSize: 20, fontWeight: FontWeight.w700),
      ),
      textTheme: const TextTheme(
        headlineMedium: TextStyle(
          color: ink,
          fontSize: 30,
          height: 1.15,
          fontWeight: FontWeight.w800,
          letterSpacing: -0.7,
        ),
        titleLarge: TextStyle(color: ink, fontSize: 19, fontWeight: FontWeight.w700),
        titleMedium: TextStyle(color: ink, fontSize: 15, fontWeight: FontWeight.w700),
        bodyLarge: TextStyle(color: ink, fontSize: 15, height: 1.45),
        bodyMedium: TextStyle(color: muted, fontSize: 13, height: 1.45),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: Colors.white,
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 15),
        hintStyle: const TextStyle(color: Color(0xFF9AA2B1), fontSize: 14),
        labelStyle: const TextStyle(color: muted, fontSize: 13, fontWeight: FontWeight.w600),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(15),
          borderSide: const BorderSide(color: border),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(15),
          borderSide: const BorderSide(color: border),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(15),
          borderSide: const BorderSide(color: violet, width: 1.5),
        ),
      ),
      filledButtonTheme: FilledButtonThemeData(
        style: FilledButton.styleFrom(
          backgroundColor: violet,
          foregroundColor: Colors.white,
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 15),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
          textStyle: const TextStyle(fontWeight: FontWeight.w700),
        ),
      ),
      outlinedButtonTheme: OutlinedButtonThemeData(
        style: OutlinedButton.styleFrom(
          foregroundColor: violet,
          padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 14),
          side: const BorderSide(color: border),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
        ),
      ),
      dividerColor: border,
    );
  }
}
