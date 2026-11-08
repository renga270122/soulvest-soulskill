import 'dart:async';
import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../models/resume_model.dart';
import '../services/api_client.dart';

class ResumeProvider extends ChangeNotifier {
  static const String _storageKey = 'soulskill.resume.draft.v2';

  ResumeModel _resume = const ResumeModel();
  bool _isLoaded = false;
  bool _isSaving = false;
  bool _isImproving = false;
  Timer? _saveTimer;
  String? _saveError;

  ResumeModel get resume => _resume;
  bool get isLoaded => _isLoaded;
  bool get isSaving => _isSaving;
  bool get isImproving => _isImproving;
  String? get saveError => _saveError;

  Future<void> load() async {
    try {
      final preferences = await SharedPreferences.getInstance();
      final encoded = preferences.getString(_storageKey);
      if (encoded != null && encoded.isNotEmpty) {
        final decoded = jsonDecode(encoded) as Map<String, dynamic>;
        _resume = ResumeModel.fromJson(decoded);
      }
    } catch (_) {
      _saveError = 'Could not load the saved draft on this device.';
    } finally {
      _isLoaded = true;
      notifyListeners();
    }
  }

  void update(ResumeModel next) {
    _resume = next.copyWith(updatedAt: DateTime.now().toIso8601String());
    _saveError = null;
    _isSaving = true;
    notifyListeners();

    _saveTimer?.cancel();
    _saveTimer = Timer(const Duration(milliseconds: 650), saveNow);
  }

  Future<void> saveNow() async {
    _saveTimer?.cancel();
    try {
      final preferences = await SharedPreferences.getInstance();
      await preferences.setString(_storageKey, jsonEncode(_resume.toJson()));
      _saveError = null;
    } catch (_) {
      _saveError = 'Draft could not be saved. Check device storage.';
    } finally {
      _isSaving = false;
      notifyListeners();
    }
  }

  Future<void> improveSummary() async {
    final summary = _resume.professionalSummary.trim();
    if (summary.isEmpty) {
      throw const ApiException('Add a short summary before asking AI to improve it.');
    }

    _isImproving = true;
    notifyListeners();
    try {
      final improved = await ApiClient().improveProfessionalSummary(
        summary: summary,
        role: _resume.targetRole,
      );
      update(_resume.copyWith(professionalSummary: improved));
      await saveNow();
    } finally {
      _isImproving = false;
      notifyListeners();
    }
  }

  @override
  void dispose() {
    _saveTimer?.cancel();
    super.dispose();
  }
}
