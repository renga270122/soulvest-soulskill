import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:provider/provider.dart';

import '../models/resume_model.dart';
import '../providers/resume_provider.dart';
import 'resume_preview_screen.dart';

class ResumeEditorScreen extends StatefulWidget {
  const ResumeEditorScreen({super.key});

  @override
  State<ResumeEditorScreen> createState() => _ResumeEditorScreenState();
}

class _ResumeEditorScreenState extends State<ResumeEditorScreen> {
  late final TextEditingController _name;
  late final TextEditingController _role;
  late final TextEditingController _email;
  late final TextEditingController _phone;
  late final TextEditingController _location;
  late final TextEditingController _summary;
  late final TextEditingController _experienceRole;
  late final TextEditingController _company;
  late final TextEditingController _experience;
  late final TextEditingController _degree;
  late final TextEditingController _institution;
  late final TextEditingController _education;
  late final TextEditingController _skills;
  final List<List<TextEditingController>> _extraExperiences = [];
  final List<List<TextEditingController>> _extraEducations = [];
  final List<List<TextEditingController>> _projects = [];
  final List<List<TextEditingController>> _certifications = [];

  @override
  void initState() {
    super.initState();
    final resume = context.read<ResumeProvider>().resume;
    _name = TextEditingController(text: resume.fullName);
    _role = TextEditingController(text: resume.targetRole);
    _email = TextEditingController(text: resume.email);
    _phone = TextEditingController(text: resume.phone);
    _location = TextEditingController(text: resume.location);
    _summary = TextEditingController(text: resume.professionalSummary);
    _experienceRole = TextEditingController(text: resume.experienceRole);
    _company = TextEditingController(text: resume.company);
    _experience = TextEditingController(text: resume.experienceDescription);
    _degree = TextEditingController(text: resume.degree);
    _institution = TextEditingController(text: resume.institution);
    _education = TextEditingController(text: resume.educationDetails);
    _skills = TextEditingController(text: resume.skills);
    for (final entry in resume.effectiveWorkExperiences.skip(1)) {
      _extraExperiences.add([
        TextEditingController(text: entry['title'] ?? ''),
        TextEditingController(text: entry['company'] ?? ''),
        TextEditingController(text: entry['description'] ?? ''),
      ]);
    }
    for (final entry in resume.projects) {
      _projects.add([TextEditingController(text: entry['name'] ?? ''), TextEditingController(text: entry['description'] ?? ''), TextEditingController(text: entry['technologies'] ?? '')]);
    }
    for (final entry in resume.certifications) {
      _certifications.add([TextEditingController(text: entry['name'] ?? ''), TextEditingController(text: entry['issuer'] ?? ''), TextEditingController(text: entry['date'] ?? '')]);
    }
    for (final entry in resume.effectiveEducationEntries.skip(1)) {
      _extraEducations.add([
        TextEditingController(text: entry['degree'] ?? ''),
        TextEditingController(text: entry['institution'] ?? ''),
        TextEditingController(text: entry['description'] ?? ''),
      ]);
    }
  }

  @override
  void dispose() {
    for (final controller in [
      _name, _role, _email, _phone, _location, _summary,
      _experienceRole, _company, _experience, _degree,
      _institution, _education, _skills,
    ]) { controller.dispose(); }
    for (final group in [..._extraExperiences, ..._extraEducations, ..._projects, ..._certifications]) {
      for (final controller in group) { controller.dispose(); }
    }
    super.dispose();
  }

  void _syncDraft() {
    final current = context.read<ResumeProvider>().resume;
    context.read<ResumeProvider>().update(
      current.copyWith(
        fullName: _name.text,
        targetRole: _role.text,
        email: _email.text,
        phone: _phone.text,
        location: _location.text,
        professionalSummary: _summary.text,
        experienceRole: _experienceRole.text,
        company: _company.text,
        experienceDescription: _experience.text,
        degree: _degree.text,
        institution: _institution.text,
        educationDetails: _education.text,
        skills: _skills.text,
        workExperiences: [
          if (_experienceRole.text.isNotEmpty || _company.text.isNotEmpty || _experience.text.isNotEmpty)
            {'title': _experienceRole.text, 'company': _company.text, 'description': _experience.text},
          ..._extraExperiences.map((g) => {'title': g[0].text, 'company': g[1].text, 'description': g[2].text}),
        ],
        projects: _projects.map((g) => {'name': g[0].text, 'description': g[1].text, 'technologies': g[2].text}).toList(),
        certifications: _certifications.map((g) => {'name': g[0].text, 'issuer': g[1].text, 'date': g[2].text}).toList(),
        educationEntries: [
          if (_degree.text.isNotEmpty || _institution.text.isNotEmpty || _education.text.isNotEmpty)
            {'degree': _degree.text, 'institution': _institution.text, 'description': _education.text},
          ..._extraEducations.map((g) => {'degree': g[0].text, 'institution': g[1].text, 'description': g[2].text}),
        ],
      ),
    );
  }


  void _addEntry(List<List<TextEditingController>> entries) {
    setState(() => entries.add(List.generate(3, (_) => TextEditingController())));
    _syncDraft();
  }

  void _removeEntry(List<List<TextEditingController>> entries, int index) {
    final removed = entries.removeAt(index);
    for (final controller in removed) { controller.dispose(); }
    setState(() {});
    _syncDraft();
  }

  Widget _additionalEntry(List<TextEditingController> fields, String title,
      List<String> labels, List<String> hints, VoidCallback onRemove) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: const Color(0xFFF8F7FF),
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: const Color(0xFFE8E5FA)),
      ),
      child: Column(children: [
        Row(children: [
          Expanded(child: Text(title, style: const TextStyle(fontWeight: FontWeight.w700))),
          IconButton(onPressed: onRemove, icon: const Icon(Icons.delete_outline, color: Colors.redAccent)),
        ]),
        for (var i = 0; i < 3; i++)
          _field(label: labels[i], controller: fields[i], hint: hints[i], lines: i == 2 ? 4 : 1),
      ]),
    );
  }

  Future<void> _importResume() async {
    try {
      final result = await FilePicker.platform.pickFiles(
        type: FileType.custom, allowedExtensions: ['pdf', 'docx', 'txt'], withData: true,
      );
      if (result == null || result.files.isEmpty) return;
      final file = result.files.single;
      final bytes = file.bytes;
      if (bytes == null || bytes.isEmpty) throw Exception('The selected file could not be read.');
      final parsed = await context.read<ResumeProvider>().parseResume(fileName: file.name, bytes: bytes);
      if (!mounted) return;
      final workCount = parsed.effectiveWorkExperiences.length;
      final educationCount = parsed.effectiveEducationEntries.length;
      final accepted = await showDialog<bool>(
        context: context,
        builder: (dialogContext) => AlertDialog(
          title: const Text('Review extracted resume details'),
          content: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(parsed.fullName.isEmpty ? 'Name not detected' : parsed.fullName,
              style: const TextStyle(fontWeight: FontWeight.w700)),
            const SizedBox(height: 8),
            Text(parsed.email.isEmpty ? 'Email not detected' : parsed.email),
            const SizedBox(height: 12),
            Text('\$workCount work experience entries'),
            Text('\$educationCount education entries'),
            Text('${parsed.skillList.length} skills'),
            Text('${parsed.certifications.length} certifications'),
            const SizedBox(height: 12),
            const Text('Importing replaces the current resume draft on this device. Review all extracted details after import.',
              style: TextStyle(fontSize: 12, color: Colors.black54)),
          ]),
          actions: [
            TextButton(onPressed: () => Navigator.pop(dialogContext, false), child: const Text('Cancel')),
            FilledButton(onPressed: () => Navigator.pop(dialogContext, true), child: const Text('Import details')),
          ],
        ),
      );
      if (accepted != true || !mounted) return;
      _applyImportedResume(parsed);
      await context.read<ResumeProvider>().importResume(parsed);
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Resume details imported. Review and correct the extracted fields.')),
      );
    } catch (error) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Could not import resume: \$error')));
    }
  }

  void _applyImportedResume(ResumeModel resume) {
    for (final group in [..._extraExperiences, ..._extraEducations, ..._projects, ..._certifications]) {
      for (final controller in group) { controller.dispose(); }
    }
    _extraExperiences.clear();
    _extraEducations.clear();
    _projects.clear();
    _certifications.clear();
    _name.text = resume.fullName;
    _role.text = resume.targetRole;
    _email.text = resume.email;
    _phone.text = resume.phone;
    _location.text = resume.location;
    _summary.text = resume.professionalSummary;
    final work = resume.effectiveWorkExperiences;
    _experienceRole.text = work.isEmpty ? '' : work.first['title'] ?? '';
    _company.text = work.isEmpty ? '' : work.first['company'] ?? '';
    _experience.text = work.isEmpty ? '' : work.first['description'] ?? '';
    final education = resume.effectiveEducationEntries;
    _degree.text = education.isEmpty ? '' : education.first['degree'] ?? '';
    _institution.text = education.isEmpty ? '' : education.first['institution'] ?? '';
    _education.text = education.isEmpty ? '' : education.first['description'] ?? '';
    _skills.text = resume.skills;
    for (final entry in work.skip(1)) {
      _extraExperiences.add([TextEditingController(text: entry['title'] ?? ''),
        TextEditingController(text: entry['company'] ?? ''), TextEditingController(text: entry['description'] ?? '')]);
    }
    for (final entry in education.skip(1)) {
      _extraEducations.add([TextEditingController(text: entry['degree'] ?? ''),
        TextEditingController(text: entry['institution'] ?? ''), TextEditingController(text: entry['description'] ?? '')]);
    }
    for (final entry in resume.projects) {
      _projects.add([TextEditingController(text: entry['name'] ?? ''),
        TextEditingController(text: entry['description'] ?? ''), TextEditingController(text: entry['technologies'] ?? '')]);
    }
    for (final entry in resume.certifications) {
      _certifications.add([TextEditingController(text: entry['name'] ?? ''),
        TextEditingController(text: entry['issuer'] ?? ''), TextEditingController(text: entry['date'] ?? '')]);
    }
    setState(() {});
  }

  Future<void> _improveSummary() async {
    final provider = context.read<ResumeProvider>();
    try {
      await provider.improveSummary();
      if (!mounted) return;
      _summary.text = provider.resume.professionalSummary;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('AI suggestion added to your draft. Please review it.')),
      );
    } catch (error) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(error.toString())));
    }
  }

  Widget _section({
    required String title,
    required String description,
    required List<Widget> children,
    IconData? icon,
  }) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(17),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: const Color(0xFFE8EAF1)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              if (icon != null) ...[
                Icon(icon, color: const Color(0xFF6558D3), size: 19),
                const SizedBox(width: 8),
              ],
              Expanded(child: Text(title, style: Theme.of(context).textTheme.titleMedium)),
            ],
          ),
          const SizedBox(height: 4),
          Text(description, style: Theme.of(context).textTheme.bodyMedium),
          const SizedBox(height: 15),
          ...children,
        ],
      ),
    );
  }

  Widget _field({
    required String label,
    required TextEditingController controller,
    required String hint,
    int lines = 1,
    TextInputType? keyboardType,
  }) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: TextField(
        controller: controller,
        minLines: lines,
        maxLines: lines,
        keyboardType: keyboardType ?? (lines > 1 ? TextInputType.multiline : TextInputType.text),
        textCapitalization: TextCapitalization.sentences,
        onChanged: (_) => _syncDraft(),
        decoration: InputDecoration(labelText: label, hintText: hint),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Resume Studio'),
        actions: [
          IconButton(
            tooltip: 'Preview resume',
            onPressed: () {
              _syncDraft();
              Navigator.of(context).push(
                MaterialPageRoute(builder: (_) => const ResumePreviewScreen()),
              );
            },
            icon: const Icon(Icons.visibility_outlined),
          ),
          const SizedBox(width: 6),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(18, 8, 18, 26),
        children: [
          Consumer<ResumeProvider>(
            builder: (context, provider, _) => Container(
              padding: const EdgeInsets.all(14),
              margin: const EdgeInsets.only(bottom: 17),
              decoration: BoxDecoration(
                color: const Color(0xFFECEAFF),
                borderRadius: BorderRadius.circular(16),
              ),
              child: Row(
                children: [
                  const Icon(Icons.cloud_done_outlined, color: Color(0xFF6558D3)),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Text(
                      provider.isSaving
                          ? 'Saving your draft on this device…'
                          : provider.saveError ?? 'Your changes save automatically on this device.',
                      style: const TextStyle(color: Color(0xFF5149A0), fontSize: 12, fontWeight: FontWeight.w600),
                    ),
                  ),
                  Text(
                    '${provider.resume.completionPercent}%',
                    style: const TextStyle(color: Color(0xFF5149A0), fontWeight: FontWeight.w800),
                  ),
                ],
              ),
            ),
          ),
          _section(
            title: 'Import an existing resume',
            description: 'Upload a PDF, DOCX or TXT file to prefill your resume. Review and edit every extracted field.',
            icon: Icons.file_upload_outlined,
            children: [
              SizedBox(width: double.infinity, child: OutlinedButton.icon(
                onPressed: _importResume,
                icon: const Icon(Icons.upload_file),
                label: const Text('Import resume file'),
              )),
              const Text('The selected file is sent to the SoulSkill parsing API for extraction.',
                style: TextStyle(fontSize: 11, color: Color(0xFF77728D))),
            ],
          ),
          _section(
            title: 'Personal details',
            description: 'The essentials recruiters need to contact you.',
            icon: Icons.person_outline_rounded,
            children: [
              _field(label: 'Full name', controller: _name, hint: 'e.g. Alex Morgan'),
              _field(label: 'Target role', controller: _role, hint: 'e.g. Senior Software Engineer'),
              _field(label: 'Email address', controller: _email, hint: 'you@example.com', keyboardType: TextInputType.emailAddress),
              _field(label: 'Phone number', controller: _phone, hint: '+91 98765 43210', keyboardType: TextInputType.phone),
              _field(label: 'City / Location', controller: _location, hint: 'Bengaluru, India'),
            ],
          ),
          _section(
            title: 'Professional summary',
            description: 'A concise introduction to your experience and strengths.',
            icon: Icons.auto_awesome_outlined,
            children: [
              _field(
                label: 'Summary',
                controller: _summary,
                hint: 'Describe your experience, strengths and the value you bring.',
                lines: 5,
              ),
              Align(
                alignment: Alignment.centerLeft,
                child: Consumer<ResumeProvider>(
                  builder: (context, provider, _) => OutlinedButton.icon(
                    onPressed: provider.isImproving ? null : _improveSummary,
                    icon: provider.isImproving
                        ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2))
                        : const Icon(Icons.auto_awesome, size: 17),
                    label: Text(provider.isImproving ? 'Improving…' : 'Improve with AI'),
                  ),
                ),
              ),
            ],
          ),
          _section(
            title: 'Work experience',
            description: 'Start with your most recent or relevant role.',
            icon: Icons.work_outline_rounded,
            children: [
              _field(label: 'Job title', controller: _experienceRole, hint: 'e.g. Software Engineer'),
              _field(label: 'Company', controller: _company, hint: 'Company name'),
              _field(
                label: 'Responsibilities and achievements',
                controller: _experience,
                hint: 'Describe what you delivered. Add measurable outcomes where possible.',
                lines: 5,
              ),
              for (var i = 0; i < _extraExperiences.length; i++)
                _additionalEntry(_extraExperiences[i], 'Additional experience ' + (i + 2).toString(),
                  const ['Job title', 'Company', 'Responsibilities and achievements'],
                  const ['e.g. Technical Lead', 'Company name', 'Describe your impact and measurable outcomes.'],
                  () => _removeEntry(_extraExperiences, i)),
              Align(alignment: Alignment.centerLeft,
                child: TextButton.icon(onPressed: () => _addEntry(_extraExperiences),
                  icon: const Icon(Icons.add), label: const Text('Add another experience'))),
            ],
          ),
          _section(
            title: 'Education',
            description: 'Add your qualification and institution.',
            icon: Icons.school_outlined,
            children: [
              _field(label: 'Degree / Qualification', controller: _degree, hint: 'e.g. B.E. Computer Science'),
              _field(label: 'Institution', controller: _institution, hint: 'College or university'),
              _field(label: 'Additional details', controller: _education, hint: 'Year, specialization, honors or relevant coursework.', lines: 3),
              for (var i = 0; i < _extraEducations.length; i++)
                _additionalEntry(_extraEducations[i], 'Additional education ' + (i + 2).toString(),
                  const ['Degree / Qualification', 'Institution', 'Additional details'],
                  const ['Qualification', 'College or university', 'Year, specialization or honors.'],
                  () => _removeEntry(_extraEducations, i)),
              Align(alignment: Alignment.centerLeft,
                child: TextButton.icon(onPressed: () => _addEntry(_extraEducations),
                  icon: const Icon(Icons.add), label: const Text('Add another education'))),
            ],
          ),
          _section(
            title: 'Projects',
            description: 'Showcase relevant work, side projects and measurable outcomes.',
            icon: Icons.code_rounded,
            children: [
              for (var i = 0; i < _projects.length; i++)
                _additionalEntry(_projects[i], 'Project ' + (i + 1).toString(),
                  const ['Project name', 'What you built and achieved', 'Technologies / tools'],
                  const ['e.g. Embedded diagnostics platform', 'Describe the problem, your contribution and impact.', 'C, C++, Python'],
                  () { final removed = _projects.removeAt(i); for (final c in removed) { c.dispose(); } setState(() {}); _syncDraft(); }),
              Align(alignment: Alignment.centerLeft,
                child: TextButton.icon(onPressed: () => _addEntry(_projects),
                  icon: const Icon(Icons.add), label: const Text('Add project'))),
            ],
          ),
          _section(
            title: 'Certifications',
            description: 'Add relevant professional certifications and courses.',
            icon: Icons.workspace_premium_outlined,
            children: [
              for (var i = 0; i < _certifications.length; i++)
                _additionalEntry(_certifications[i], 'Certification ' + (i + 1).toString(),
                  const ['Certification name', 'Issuing organisation', 'Date / year'],
                  const ['e.g. AWS Certified Developer', 'e.g. Amazon Web Services', '2026'],
                  () { final removed = _certifications.removeAt(i); for (final c in removed) { c.dispose(); } setState(() {}); _syncDraft(); }),
              Align(alignment: Alignment.centerLeft,
                child: TextButton.icon(onPressed: () => _addEntry(_certifications),
                  icon: const Icon(Icons.add), label: const Text('Add certification'))),
            ],
          ),
          _section(
            title: 'Skills',
            description: 'Separate skills with commas. You can refine the list later.',
            icon: Icons.bolt_outlined,
            children: [
              _field(label: 'Skills', controller: _skills, hint: 'C++, Python, Embedded Linux, Communication', lines: 3),
            ],
          ),
          const SizedBox(height: 2),
          FilledButton.icon(
            onPressed: () async {
              _syncDraft();
              await context.read<ResumeProvider>().saveNow();
              if (!context.mounted) return;
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Your resume draft is saved on this device.')),
              );
            },
            icon: const Icon(Icons.check_circle_outline),
            label: const Text('Save draft'),
          ),
          const SizedBox(height: 10),
          Text(
            'AI-generated suggestions are drafts. Review every detail for accuracy before using your resume.',
            textAlign: TextAlign.center,
            style: Theme.of(context).textTheme.bodyMedium,
          ),
        ],
      ),
    );
  }
}
