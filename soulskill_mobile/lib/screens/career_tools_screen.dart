import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:provider/provider.dart';

import '../providers/resume_provider.dart';

enum CareerTool { jobFit, tracker, interview }

class CareerToolsScreen extends StatefulWidget {
  const CareerToolsScreen({super.key, this.initialTool = CareerTool.jobFit});
  final CareerTool initialTool;

  @override
  State<CareerToolsScreen> createState() => _CareerToolsScreenState();
}

class _CareerToolsScreenState extends State<CareerToolsScreen> {
  late CareerTool _tool;
  final _role = TextEditingController();
  final _description = TextEditingController();
  final _company = TextEditingController();
  final _answer = TextEditingController();
  final List<Map<String, String>> _applications = [];
  String _status = 'Applied';
  bool _loading = true;
  bool _analyzed = false;
  List<String> _matched = [];
  List<String> _missing = [];

  static const _trackerKey = 'soulskill.application.tracker.v1';
  static const _questions = [
    'Tell me about yourself and the value you bring to this role.',
    'Describe a challenging problem you solved. What was your approach?',
    'Tell me about a time you had to work with a difficult stakeholder.',
    'Describe a project where you improved quality, performance or delivery.',
    'What is one skill you are actively developing, and why?',
    'Why are you interested in this role and this organisation?',
  ];

  @override
  void initState() {
    super.initState();
    _tool = widget.initialTool;
    _loadApplications();
  }

  @override
  void dispose() {
    _role.dispose();
    _description.dispose();
    _company.dispose();
    _answer.dispose();
    super.dispose();
  }

  Future<void> _loadApplications() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final raw = prefs.getString(_trackerKey);
      if (raw != null) {
        final items = (jsonDecode(raw) as List).whereType<Map>();
        _applications
          ..clear()
          ..addAll(items.map((item) => item.map((k, v) =>
              MapEntry(k.toString(), v.toString()))));
      }
    } catch (_) {
      // Keep the tracker usable even if an old local draft cannot be read.
    }
    if (mounted) setState(() => _loading = false);
  }

  Future<void> _saveApplications() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_trackerKey, jsonEncode(_applications));
  }

  List<String> _tokens(String text) => RegExp(r"[a-zA-Z][a-zA-Z0-9+#.\-]{1,}")
      .allMatches(text.toLowerCase())
      .map((m) => m.group(0)!)
      .where((word) => !_stopWords.contains(word))
      .toSet()
      .toList();

  static const _stopWords = {
    'the','and','for','with','you','your','are','our','this','that','will',
    'from','have','has','was','were','who','what','when','where','how','can',
    'able','into','about','their','they','them','then','than','also','not',
    'but','all','any','per','use','using','used','role','work','working',
    'years','year','strong','good','excellent','required','preferred',
    'experience','skills','skill','knowledge','ability','team','teams'
  };

  void _analyze() {
    final jd = _tokens(_description.text);
    if (_description.text.trim().length < 40) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Paste a fuller job description (at least 40 characters).')),
      );
      return;
    }
    final resume = context.read<ResumeProvider>().resume;
    final evidence = _tokens([
      resume.targetRole, resume.professionalSummary, resume.experienceRole,
      resume.company, resume.experienceDescription, resume.skills,
      resume.degree, resume.institution, resume.educationDetails
    ].join(' ')).toSet();
    setState(() {
      _matched = jd.where(evidence.contains).toList()..sort();
      _missing = jd.where((word) => !evidence.contains(word)).toList()..sort();
      _analyzed = true;
    });
  }

  Future<void> _addApplication() async {
    if (_role.text.trim().isEmpty || _company.text.trim().isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Add both a role and a company.')),
      );
      return;
    }
    setState(() {
      _applications.insert(0, {
        'role': _role.text.trim(),
        'company': _company.text.trim(),
        'status': _status,
        'added': DateTime.now().toIso8601String(),
      });
      _role.clear();
      _company.clear();
    });
    await _saveApplications();
  }

  Future<void> _removeApplication(int index) async {
    setState(() => _applications.removeAt(index));
    await _saveApplications();
  }

  @override
  Widget build(BuildContext context) {
    final tabs = [
      (CareerTool.jobFit, 'Job matching', Icons.track_changes_outlined),
      (CareerTool.tracker, 'Applications', Icons.view_kanban_outlined),
      (CareerTool.interview, 'Interview', Icons.record_voice_over_outlined),
    ];
    return Scaffold(
      appBar: AppBar(title: const Text('Career tools')),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(18, 8, 18, 28),
        children: [
          Text('Turn preparation into progress',
              style: Theme.of(context).textTheme.headlineSmall),
          const SizedBox(height: 6),
          const Text('Practical tools for your next career move.',
              style: TextStyle(color: Color(0xFF77728D), height: 1.4)),
          const SizedBox(height: 18),
          SegmentedButton<CareerTool>(
            segments: tabs.map((tab) => ButtonSegment<CareerTool>(
              value: tab.$1, icon: Icon(tab.$3), label: Text(tab.$2),
            )).toList(),
            selected: {_tool},
            onSelectionChanged: (selection) => setState(() {
              _tool = selection.first;
              _analyzed = false;
            }),
            showSelectedIcon: false,
          ),
          const SizedBox(height: 18),
          if (_tool == CareerTool.jobFit) _jobFitView(),
          if (_tool == CareerTool.tracker) _trackerView(),
          if (_tool == CareerTool.interview) _interviewView(),
        ],
      ),
    );
  }

  Widget _panel({required Widget child}) => Container(
    width: double.infinity,
    padding: const EdgeInsets.all(17),
    decoration: BoxDecoration(
      color: Colors.white,
      borderRadius: BorderRadius.circular(18),
      border: Border.all(color: const Color(0xFFE8E6F2)),
    ),
    child: child,
  );

  Widget _jobFitView() {
    final resume = context.watch<ResumeProvider>().resume;
    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      _panel(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        const Text('Compare your experience with a real role',
            style: TextStyle(fontSize: 17, fontWeight: FontWeight.w800)),
        const SizedBox(height: 6),
        Text('Current resume: ${resume.completionPercent}% complete',
            style: const TextStyle(color: Color(0xFF77728D), fontSize: 12)),
        const SizedBox(height: 14),
        TextField(controller: _description, minLines: 7, maxLines: 12,
          decoration: const InputDecoration(
            hintText: 'Paste the job description here…',
            border: OutlineInputBorder(), alignLabelWithHint: true,
          )),
        const SizedBox(height: 13),
        SizedBox(width: double.infinity, child: FilledButton.icon(
          onPressed: _analyze, icon: const Icon(Icons.analytics_outlined),
          label: const Text('Compare with my resume'),
        )),
      ])),
      if (_analyzed) ...[
        const SizedBox(height: 12),
        _panel(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          const Text('Keyword evidence review',
              style: TextStyle(fontSize: 17, fontWeight: FontWeight.w800)),
          const SizedBox(height: 5),
          Text('${_matched.length} of ${_matched.length + _missing.length} distinct job terms found in your current resume text.',
              style: const TextStyle(color: Color(0xFF77728D), fontSize: 12)),
          const SizedBox(height: 15),
          const Text('Found in your resume', style: TextStyle(fontWeight: FontWeight.w700, color: Color(0xFF287A59))),
          const SizedBox(height: 7),
          _chips(_matched, const Color(0xFF287A59)),
          const SizedBox(height: 15),
          const Text('Not found — review manually', style: TextStyle(fontWeight: FontWeight.w700, color: Color(0xFF9A641B))),
          const SizedBox(height: 7),
          _chips(_missing, const Color(0xFF9A641B)),
          const SizedBox(height: 12),
          const Text('This is a simple local keyword comparison, not an ATS score or AI assessment. Add a missing term only when it accurately describes your experience.',
              style: TextStyle(fontSize: 11, color: Color(0xFF77728D), height: 1.4)),
        ])),
      ],
    ]);
  }

  Widget _chips(List<String> words, Color color) => words.isEmpty
      ? const Text('No terms in this group.', style: TextStyle(color: Color(0xFF77728D), fontSize: 12))
      : Wrap(spacing: 6, runSpacing: 6, children: words.take(50).map((word) => Chip(
          label: Text(word, style: TextStyle(fontSize: 11, color: color)),
          backgroundColor: color.withValues(alpha: 0.08),
          side: BorderSide(color: color.withValues(alpha: 0.18)),
          visualDensity: VisualDensity.compact,
        )).toList());

  Widget _trackerView() => Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
    _panel(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      const Text('Add an opportunity', style: TextStyle(fontSize: 17, fontWeight: FontWeight.w800)),
      const SizedBox(height: 12),
      TextField(controller: _role, decoration: const InputDecoration(labelText: 'Job title / role', border: OutlineInputBorder())),
      const SizedBox(height: 10),
      TextField(controller: _company, decoration: const InputDecoration(labelText: 'Company', border: OutlineInputBorder())),
      const SizedBox(height: 10),
      DropdownButtonFormField<String>(
        value: _status,
        decoration: const InputDecoration(labelText: 'Application stage', border: OutlineInputBorder()),
        items: const ['Interested', 'Applied', 'Assessment', 'Interview', 'Offer', 'Rejected']
            .map((value) => DropdownMenuItem(value: value, child: Text(value))).toList(),
        onChanged: (value) => setState(() => _status = value ?? 'Applied'),
      ),
      const SizedBox(height: 12),
      SizedBox(width: double.infinity, child: FilledButton.icon(
        onPressed: _addApplication, icon: const Icon(Icons.add),
        label: const Text('Save application'),
      )),
      const SizedBox(height: 5),
      const Text('Saved on this device only. No account or cloud sync is connected yet.',
          style: TextStyle(fontSize: 11, color: Color(0xFF77728D))),
    ])),
    const SizedBox(height: 14),
    Row(children: [
      const Expanded(child: Text('Your applications', style: TextStyle(fontSize: 17, fontWeight: FontWeight.w800))),
      Text('${_applications.length}', style: const TextStyle(color: Color(0xFF6558D3), fontWeight: FontWeight.w800)),
    ]),
    const SizedBox(height: 9),
    if (_loading) const Center(child: CircularProgressIndicator())
    else if (_applications.isEmpty)
      _panel(child: const Text('No applications yet. Add the first role you are exploring.',
          style: TextStyle(color: Color(0xFF77728D))))
    else ..._applications.asMap().entries.map((entry) {
      final item = entry.value;
      return Padding(padding: const EdgeInsets.only(bottom: 9), child: _panel(child: Row(
        children: [
          const CircleAvatar(backgroundColor: Color(0xFFECEAFF),
            child: Icon(Icons.business_center_outlined, color: Color(0xFF6558D3))),
          const SizedBox(width: 12),
          Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(item['role'] ?? '', style: const TextStyle(fontWeight: FontWeight.w800)),
            Text(item['company'] ?? '', style: const TextStyle(color: Color(0xFF77728D), fontSize: 12)),
            const SizedBox(height: 5),
            Text(item['status'] ?? 'Applied', style: const TextStyle(color: Color(0xFF6558D3), fontSize: 11, fontWeight: FontWeight.w700)),
          ])),
          IconButton(tooltip: 'Remove application', onPressed: () => _removeApplication(entry.key),
            icon: const Icon(Icons.delete_outline, color: Color(0xFF8B849F))),
        ],
      )));
    }),
  ]);

  Widget _interviewView() {
    final question = _questions[_questionIndex % _questions.length];
    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      _panel(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        const Text('Practice one answer at a time', style: TextStyle(fontSize: 17, fontWeight: FontWeight.w800)),
        const SizedBox(height: 6),
        const Text('Use the STAR structure: Situation, Task, Action and Result. Your notes stay in this screen and are not sent to a server.',
            style: TextStyle(color: Color(0xFF77728D), fontSize: 12, height: 1.45)),
        const SizedBox(height: 18),
        Text('QUESTION ${_questionIndex + 1} OF ${_questions.length}',
            style: const TextStyle(color: Color(0xFF6558D3), fontWeight: FontWeight.w800, fontSize: 10, letterSpacing: 1)),
        const SizedBox(height: 9),
        Text(question, style: const TextStyle(fontSize: 19, height: 1.3, fontWeight: FontWeight.w800)),
        const SizedBox(height: 16),
        TextField(controller: _answer, minLines: 6, maxLines: 10,
          decoration: const InputDecoration(
            labelText: 'Draft your answer using STAR',
            hintText: 'Situation…\nTask…\nAction…\nResult…',
            border: OutlineInputBorder(), alignLabelWithHint: true,
          )),
        const SizedBox(height: 14),
        Row(children: [
          OutlinedButton.icon(onPressed: () => setState(() {
            _questionIndex = (_questionIndex - 1 + _questions.length) % _questions.length;
            _answer.clear();
          }), icon: const Icon(Icons.chevron_left), label: const Text('Previous')),
          const Spacer(),
          FilledButton.icon(onPressed: () => setState(() {
            _questionIndex = (_questionIndex + 1) % _questions.length;
            _answer.clear();
          }), icon: const Icon(Icons.chevron_right), label: const Text('Next question')),
        ]),
      ])),
      const SizedBox(height: 12),
      _panel(child: const Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text('Quick self-review', style: TextStyle(fontWeight: FontWeight.w800)),
        SizedBox(height: 8),
        Text('• Did I explain the context clearly?\n• Was my personal contribution specific?\n• Did I include a measurable or observable result?\n• Is the example relevant to the target role?',
            style: TextStyle(color: Color(0xFF77728D), fontSize: 12, height: 1.6)),
      ])),
    ]);
  }

  int _questionIndex = 0;
}
