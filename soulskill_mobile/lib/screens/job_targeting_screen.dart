import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../providers/resume_provider.dart';
import 'resume_preview_screen.dart';
import 'resume_editor_screen.dart';

class JobTargetingScreen extends StatefulWidget {
  const JobTargetingScreen({super.key});

  @override
  State<JobTargetingScreen> createState() => _JobTargetingScreenState();
}

class _JobTargetingScreenState extends State<JobTargetingScreen> {
  late final TextEditingController _roleController;
  late final TextEditingController _jobDescriptionController;
  Map<String, dynamic>? _analysis;
  bool _isUploading = false;
  bool _isAnalyzing = false;
  bool _isApplying = false;
  String? _fileName;

  @override
  void initState() {
    super.initState();
    final resume = context.read<ResumeProvider>().resume;
    _roleController = TextEditingController(text: resume.targetRole);
    _jobDescriptionController = TextEditingController();
  }

  @override
  void dispose() {
    _roleController.dispose();
    _jobDescriptionController.dispose();
    super.dispose();
  }

  void _showMessage(String message) {
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(message)));
  }

  Future<void> _importResume() async {
    try {
      final picked = await FilePicker.pickFiles(
        type: FileType.custom,
        allowedExtensions: ['pdf', 'docx', 'txt'],
        allowMultiple: false,
        withData: true,
      );
      if (picked == null || picked.files.isEmpty) return;

      final file = picked.files.single;
      if (file.size > 5 * 1024 * 1024) {
        _showMessage('Choose a resume smaller than 5 MB.');
        return;
      }
      final bytes = file.bytes;
      if (bytes == null || bytes.isEmpty) {
        _showMessage('The selected file could not be read. Try another file.');
        return;
      }

      setState(() {
        _isUploading = true;
        _fileName = file.name;
        _analysis = null;
      });

      final response = await context.read<ResumeProvider>().importResumeFile(
            bytes: bytes,
            fileName: file.name,
          );
      final parsed = response['resume'] as Map<String, dynamic>? ?? {};
      final current = context.read<ResumeProvider>().resume;
      String value(String key, String fallback) {
        final extracted = parsed[key]?.toString().trim() ?? '';
        return extracted.isEmpty ? fallback : extracted;
      }

      final imported = current.copyWith(
        fullName: value('fullName', current.fullName),
        email: value('email', current.email),
        phone: value('phone', current.phone),
        location: value('location', current.location),
        professionalSummary: value('professionalSummary', current.professionalSummary),
        experienceRole: value('experienceRole', current.experienceRole),
        company: value('company', current.company),
        experienceDescription: value('experienceDescription', current.experienceDescription),
        degree: value('degree', current.degree),
        institution: value('institution', current.institution),
        educationDetails: value('educationDetails', current.educationDetails),
        skills: value('skills', current.skills),
      );
      final provider = context.read<ResumeProvider>();
      provider.update(imported);
      await provider.saveNow();

      if (!mounted) return;
      setState(() => _isUploading = false);
      _showMessage('Resume imported. Please review the extracted details in Resume Studio.');
    } catch (error) {
      if (!mounted) return;
      setState(() => _isUploading = false);
      _showMessage(error.toString());
    }
  }

  Future<void> _analyze() async {
    final jobDescription = _jobDescriptionController.text.trim();
    final targetRole = _roleController.text.trim();
    if (jobDescription.length < 50) {
      _showMessage('Paste the full job description (at least 50 characters).');
      return;
    }
    if (context.read<ResumeProvider>().resume.completionPercent == 0) {
      _showMessage('Import a resume or add your details in Resume Studio first.');
      return;
    }

    setState(() {
      _isAnalyzing = true;
      _analysis = null;
    });
    try {
      final result = await context.read<ResumeProvider>().analyzeJobFit(
            jobDescription: jobDescription,
            targetRole: targetRole,
          );
      if (!mounted) return;
      setState(() {
        _analysis = result;
        _isAnalyzing = false;
      });
    } catch (error) {
      if (!mounted) return;
      setState(() => _isAnalyzing = false);
      _showMessage(error.toString());
    }
  }

  Future<void> _applyTailoring() async {
    final result = _analysis;
    if (result == null) return;
    final tailored = result['tailored_resume'];
    if (tailored is! Map<String, dynamic>) {
      _showMessage('The tailored draft is not available. Please analyze again.');
      return;
    }

    setState(() => _isApplying = true);
    try {
      await context.read<ResumeProvider>().applyTailoredResume(tailored);
      if (!mounted) return;
      setState(() => _isApplying = false);
      _showMessage('Job-specific ordering applied. No missing skills were added.');
    } catch (error) {
      if (!mounted) return;
      setState(() => _isApplying = false);
      _showMessage('Could not save the tailored draft: ' + error.toString());
    }
  }

  List<String> _terms(String key) {
    final value = _analysis?[key];
    if (value is! List) return [];
    return value.map((item) => item.toString()).toList();
  }

  Widget _keywordChips(List<String> terms, Color color) {
    if (terms.isEmpty) {
      return const Text('None identified', style: TextStyle(color: Color(0xFF77728D), fontSize: 13));
    }
    return Wrap(
      spacing: 7,
      runSpacing: 7,
      children: terms.map((term) => Chip(
        label: Text(term, style: TextStyle(color: color, fontSize: 12, fontWeight: FontWeight.w600)),
        backgroundColor: color.withValues(alpha: 0.08),
        side: BorderSide(color: color.withValues(alpha: 0.16)),
        visualDensity: VisualDensity.compact,
        materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
      )).toList(),
    );
  }

  Widget _sectionTitle(String title, String description) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w800, color: Color(0xFF252442))),
          const SizedBox(height: 3),
          Text(description, style: const TextStyle(fontSize: 12, color: Color(0xFF77728D), height: 1.4)),
        ],
      ),
    );
  }

  Widget _panel({required Widget child}) {
    return Container(
      width: double.infinity,
      margin: const EdgeInsets.only(bottom: 14),
      padding: const EdgeInsets.all(17),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(18),
        border: Border.all(color: const Color(0xFFE8E6F2)),
      ),
      child: child,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Resume to Interview'),
        actions: [
          IconButton(
            tooltip: 'Preview resume',
            onPressed: () => Navigator.of(context).push(
              MaterialPageRoute(builder: (_) => const ResumePreviewScreen()),
            ),
            icon: const Icon(Icons.visibility_outlined),
          ),
          const SizedBox(width: 6),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(18, 8, 18, 28),
        children: [
          _panel(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Row(
                  children: [
                    Icon(Icons.track_changes_rounded, color: Color(0xFF6558D3), size: 22),
                    SizedBox(width: 9),
                    Expanded(child: Text('Start with one real opportunity', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800, color: Color(0xFF252442)))),
                  ],
                ),
                const SizedBox(height: 7),
                const Text(
                  'Compare your current resume with a job description. SoulSkill will highlight relevant evidence, identify terms to review and help you prioritize what is already true about your experience.',
                  style: TextStyle(fontSize: 13, height: 1.5, color: Color(0xFF77728D)),
                ),
                const SizedBox(height: 14),
                OutlinedButton.icon(
                  onPressed: _isUploading ? null : _importResume,
                  icon: _isUploading
                      ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2))
                      : const Icon(Icons.upload_file_rounded),
                  label: Text(_isUploading ? 'Importing resume…' : 'Import PDF, DOCX or TXT resume'),
                ),
                if (_fileName != null) ...[
                  const SizedBox(height: 6),
                  Text('Selected: ' + _fileName!, style: const TextStyle(fontSize: 11, color: Color(0xFF6558D3))),
                ],
                const SizedBox(height: 2),
                TextButton(
                  onPressed: () => Navigator.of(context).push(
                    MaterialPageRoute(builder: (_) => const ResumePreviewScreen()),
                  ),
                  child: const Text('Preview current resume'),
                ),
                TextButton.icon(
                  onPressed: () => Navigator.of(context).push(
                    MaterialPageRoute(builder: (_) => const ResumeEditorScreen()),
                  ),
                  icon: const Icon(Icons.edit_outlined, size: 17),
                  label: const Text('Review or edit imported details'),
                ),
              ],
            ),
          ),
          _panel(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _sectionTitle('Target role', 'Name the position you want to apply for.'),
                TextField(
                  controller: _roleController,
                  textCapitalization: TextCapitalization.words,
                  decoration: const InputDecoration(
                    hintText: 'e.g. Senior Embedded Software Engineer',
                    prefixIcon: Icon(Icons.work_outline_rounded),
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 18),
                _sectionTitle('Job description', 'Paste the job posting text. Do not include confidential information.'),
                TextField(
                  controller: _jobDescriptionController,
                  minLines: 8,
                  maxLines: 14,
                  textCapitalization: TextCapitalization.sentences,
                  decoration: const InputDecoration(
                    hintText: 'Paste responsibilities, required skills and qualifications here…',
                    alignLabelWithHint: true,
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 14),
                SizedBox(
                  width: double.infinity,
                  child: FilledButton.icon(
                    onPressed: _isAnalyzing ? null : _analyze,
                    icon: _isAnalyzing
                        ? const SizedBox(width: 17, height: 17, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                        : const Icon(Icons.search_rounded),
                    label: Text(_isAnalyzing ? 'Analyzing job fit…' : 'Analyze my job fit'),
                  ),
                ),
              ],
            ),
          ),
          if (_analysis != null) ...[
            _panel(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _sectionTitle('Your job alignment', 'A transparent keyword comparison, not a prediction of interview selection.'),
                  Row(
                    crossAxisAlignment: CrossAxisAlignment.end,
                    children: [
                      Text(
                        ((_analysis!['keyword_match_percent'] as num?)?.round() ?? 0).toString() + '%',
                        style: const TextStyle(fontSize: 34, fontWeight: FontWeight.w900, color: Color(0xFF5142C5)),
                      ),
                      const SizedBox(width: 10),
                      const Padding(
                        padding: EdgeInsets.only(bottom: 7),
                        child: Text('keyword coverage', style: TextStyle(fontSize: 12, color: Color(0xFF77728D))),
                      ),
                    ],
                  ),
                  const SizedBox(height: 10),
                  ClipRRect(
                    borderRadius: BorderRadius.circular(10),
                    child: LinearProgressIndicator(
                      minHeight: 9,
                      value: ((_analysis!['keyword_match_percent'] as num?)?.toDouble() ?? 0) / 100,
                      backgroundColor: const Color(0xFFECEAF5),
                      color: const Color(0xFF6558D3),
                    ),
                  ),
                  const SizedBox(height: 9),
                  Text(
                    ((_analysis!['matched_keyword_count'] ?? 0).toString()) + ' of ' + ((_analysis!['total_keyword_count'] ?? 0).toString()) + ' job terms found in your resume',
                    style: const TextStyle(fontSize: 12, color: Color(0xFF77728D)),
                  ),
                ],
              ),
            ),
            _panel(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _sectionTitle('Evidence already present', 'These job terms were found in the resume content you provided.'),
                  _keywordChips(_terms('matched_keywords'), const Color(0xFF287A59)),
                  const SizedBox(height: 18),
                  _sectionTitle('Terms to review', 'They were not found in your resume. Add them only if you genuinely have this skill or experience.'),
                  _keywordChips(_terms('missing_keywords'), const Color(0xFF9A641B)),
                ],
              ),
            ),
            _panel(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _sectionTitle('Recommended improvements', 'Use these as a checklist before applying.'),
                  ..._terms('recommendations').map((item) => Padding(
                    padding: const EdgeInsets.only(bottom: 10),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Icon(Icons.check_circle_outline, size: 18, color: Color(0xFF6558D3)),
                        const SizedBox(width: 9),
                        Expanded(child: Text(item, style: const TextStyle(fontSize: 13, height: 1.45, color: Color(0xFF42405C)))),
                      ],
                    ),
                  )),
                  const SizedBox(height: 4),
                  FilledButton.icon(
                    onPressed: _isApplying ? null : _applyTailoring,
                    icon: _isApplying
                        ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                        : const Icon(Icons.auto_fix_high_rounded),
                    label: Text(_isApplying ? 'Applying…' : 'Apply safe tailoring'),
                  ),
                  const SizedBox(height: 8),
                  OutlinedButton.icon(
                    onPressed: () => Navigator.of(context).push(
                      MaterialPageRoute(builder: (_) => const ResumePreviewScreen()),
                    ),
                    icon: const Icon(Icons.picture_as_pdf_outlined),
                    label: const Text('Preview and export resume'),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    _analysis!['fact_integrity']?.toString() ?? 'Only existing resume information is used.',
                    style: const TextStyle(fontSize: 11, color: Color(0xFF77728D), height: 1.4),
                  ),
                ],
              ),
            ),
          ],
          const Padding(
            padding: EdgeInsets.symmetric(horizontal: 5, vertical: 3),
            child: Text(
              'SoulSkill cannot guarantee interview calls. Hiring decisions depend on many factors beyond a resume. Keep every statement accurate and review the final document before sending it.',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 11, color: Color(0xFF858197), height: 1.45),
            ),
          ),
        ],
      ),
    );
  }
}
