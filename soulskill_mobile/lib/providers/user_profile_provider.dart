import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../models/user_profile_model.dart';

class UserProfileProvider extends ChangeNotifier {
  static const String _profileKey = 'soulskill.user.profile.v1';
  static const String _onboardingKey = 'soulskill.onboarding.completed.v1';

  UserProfileModel _profile = const UserProfileModel();
  bool _isLoaded = false;
  bool _isSaving = false;
  bool _hasCompletedOnboarding = false;
  String? _saveError;

  UserProfileModel get profile => _profile;
  bool get isLoaded => _isLoaded;
  bool get isSaving => _isSaving;
  bool get hasCompletedOnboarding => _hasCompletedOnboarding;
  String? get saveError => _saveError;

  Future<void> load() async {
    try {
      final preferences = await SharedPreferences.getInstance();
      final encoded = preferences.getString(_profileKey);
      if (encoded != null && encoded.isNotEmpty) {
        final decoded = jsonDecode(encoded) as Map<String, dynamic>;
        _profile = UserProfileModel.fromJson(decoded);
      }
      _hasCompletedOnboarding =
          preferences.getBool(_onboardingKey) ?? false;
    } catch (_) {
      _saveError = 'Could not load your profile from this device.';
    } finally {
      _isLoaded = true;
      notifyListeners();
    }
  }

  Future<void> saveProfile(
    UserProfileModel next, {
    bool completeOnboarding = true,
  }) async {
    _isSaving = true;
    _saveError = null;
    notifyListeners();

    try {
      final updated = next.copyWith(
        updatedAt: DateTime.now().toIso8601String(),
      );
      final preferences = await SharedPreferences.getInstance();
      await preferences.setString(_profileKey, jsonEncode(updated.toJson()));
      if (completeOnboarding) {
        await preferences.setBool(_onboardingKey, true);
      }

      _profile = updated;
      _hasCompletedOnboarding =
          completeOnboarding || _hasCompletedOnboarding;
    } catch (_) {
      _saveError = 'Your profile could not be saved. Please try again.';
      rethrow;
    } finally {
      _isSaving = false;
      notifyListeners();
    }
  }
}
