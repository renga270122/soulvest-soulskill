import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';

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
  final ApiClient _apiClient = ApiClient();

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
      final improved = await _apiClient.improveProfessionalSummary(
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


  Future<Map<String, dynamic>> analyzeJobFit({
    required String jobDescription,
    required String targetRole,
  }) {
    return _apiClient.analyzeResumeForJob(
      resume: _resume,
      jobDescription: jobDescription,
      targetRole: targetRole,
    );
  }

  Future<Map<String, dynamic>> importResumeFile({
    required Uint8List bytes,
    required String fileName,
  }) {
    return _apiClient.parseResumeFile(bytes: bytes, fileName: fileName);
  }

  Future<void> applyTailoredResume(Map<String, dynamic> tailored) async {
    final rawSkills = tailored['skills'];
    final skills = rawSkills is List
        ? rawSkills.map((value) => value.toString().trim()).where((value) => value.isNotEmpty).join(', ')
        : _resume.skills;
    update(
      _resume.copyWith(
        targetRole: (tailored['target_role'] as String?)?.trim().isNotEmpty == true
            ? (tailored['target_role'] as String).trim()
            : _resume.targetRole,
        professionalSummary: (tailored['professional_summary'] as String?)?.trim().isNotEmpty == true
            ? (tailored['professional_summary'] as String).trim()
            : _resume.professionalSummary,
        experienceDescription: (tailored['experience_description'] as String?)?.trim().isNotEmpty == true
            ? (tailored['experience_description'] as String).trim()
            : _resume.experienceDescription,
        skills: skills,
      ),
    );
    await saveNow();
  }

  @override
  void dispose() {
    _saveTimer?.cancel();
    _apiClient.close();
    super.dispose();
  }
}
