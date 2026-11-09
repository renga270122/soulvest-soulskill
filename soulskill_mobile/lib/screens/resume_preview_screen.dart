import 'package:flutter/material.dart';
import 'package:pdf/pdf.dart';
import 'package:pdf/widgets.dart' as pw;
import 'package:printing/printing.dart';
import 'package:provider/provider.dart';

import '../models/resume_model.dart';
import '../providers/resume_provider.dart';

enum ResumeTemplate { modern, classic, minimal }

class ResumePreviewScreen extends StatefulWidget {
  const ResumePreviewScreen({super.key});

  @override
  State<ResumePreviewScreen> createState() => _ResumePreviewScreenState();
}

class _ResumePreviewScreenState extends State<ResumePreviewScreen> {
  ResumeTemplate _template = ResumeTemplate.modern;
  bool _exporting = false;

  String get _templateName => switch (_template) {
    ResumeTemplate.modern => 'Modern',
    ResumeTemplate.classic => 'Classic',
    ResumeTemplate.minimal => 'Minimal',
  };

  Future<void> _exportPdf(ResumeModel resume) async {
    setState(() => _exporting = true);
    try {
      final document = pw.Document();
      final accent = switch (_template) {
        ResumeTemplate.modern => PdfColor.fromHex('#6558D3'),
        ResumeTemplate.classic => PdfColor.fromHex('#243B53'),
        ResumeTemplate.minimal => PdfColor.fromHex('#333333'),
      };
      final contact = [resume.email, resume.phone, resume.location]
          .where((value) => value.trim().isNotEmpty).join('  |  ');
      final sections = <pw.Widget>[];
      void section(String title, String body, {String heading = ''}) {
        if (body.trim().isEmpty && heading.trim().isEmpty) return;
        sections.add(pw.SizedBox(height: 13));
        sections.add(pw.Text(title.toUpperCase(), style: pw.TextStyle(
          fontSize: 9, fontWeight: pw.FontWeight.bold, color: accent,
          letterSpacing: 1.1,
        )));
        if (heading.trim().isNotEmpty) {
          sections.add(pw.SizedBox(height: 4));
          sections.add(pw.Text(heading, style: pw.TextStyle(
            fontSize: 10, fontWeight: pw.FontWeight.bold,
          )));
        }
        if (body.trim().isNotEmpty) {
          sections.add(pw.SizedBox(height: 3));
          sections.add(pw.Text(body, style: const pw.TextStyle(fontSize: 9, lineSpacing: 2)));
        }
      }

      section('Professional summary', resume.professionalSummary);
      for (final entry in resume.effectiveWorkExperiences) {
        final heading = [entry['title'] ?? '', entry['company'] ?? '']
            .where((value) => value.isNotEmpty).join('  |  ');
        final dates = [entry['start_date'] ?? '', entry['end_date'] ?? '']
            .where((value) => value.isNotEmpty).join(' – ');
        section('Experience', [entry['description'] ?? '', dates]
            .where((value) => value.isNotEmpty).join('\n'), heading: heading);
      }
      for (final entry in resume.effectiveEducationEntries) {
        section('Education', entry['description'] ?? '',
          heading: [entry['degree'] ?? '', entry['institution'] ?? '']
              .where((value) => value.isNotEmpty).join('  |  '));
      }
      for (final entry in resume.projects) {
        section('Project', [entry['description'] ?? '', entry['technologies'] ?? '']
            .where((value) => value.isNotEmpty).join('\n'),
          heading: entry['name'] ?? '');
      }
      for (final entry in resume.certifications) {
        section('Certification', [entry['issuer'] ?? '', entry['date'] ?? '']
            .where((value) => value.isNotEmpty).join('  |  '),
          heading: entry['name'] ?? '');
      }
      section('Skills', resume.skillList.join('  •  '));

      document.addPage(pw.MultiPage(
        pageFormat: PdfPageFormat.a4,
        margin: const pw.EdgeInsets.fromLTRB(42, 44, 42, 44),
        build: (_) => [
          pw.Text(resume.fullName.isEmpty ? 'Your Name' : resume.fullName,
            style: pw.TextStyle(fontSize: 22, fontWeight: pw.FontWeight.bold, color: accent)),
          if (resume.targetRole.isNotEmpty) ...[
            pw.SizedBox(height: 4),
            pw.Text(resume.targetRole, style: pw.TextStyle(fontSize: 11, color: accent)),
          ],
          if (contact.isNotEmpty) ...[
            pw.SizedBox(height: 7),
            pw.Text(contact, style: const pw.TextStyle(fontSize: 8, color: PdfColors.grey700)),
          ],
          pw.SizedBox(height: 12),
          pw.Divider(color: accent, thickness: 1.2),
          ...sections,
        ],
      ));
      await Printing.layoutPdf(
        name: 'soulskill_resume_${resume.fullName.trim().replaceAll(RegExp(r'[^a-zA-Z0-9]+'), '_').toLowerCase()}',
        onLayout: (_) async => document.save(),
      );
    } catch (error) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('PDF export failed: $error')),
      );
    } finally {
      if (mounted) setState(() => _exporting = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<ResumeProvider>(
      builder: (context, provider, _) {
        return Scaffold(
          appBar: AppBar(
            title: const Text('Resume preview'),
            actions: [
              PopupMenuButton<ResumeTemplate>(
                tooltip: 'Choose template',
                initialValue: _template,
                onSelected: (value) => setState(() => _template = value),
                itemBuilder: (_) => const [
                  PopupMenuItem(value: ResumeTemplate.modern, child: Text('Modern')),
                  PopupMenuItem(value: ResumeTemplate.classic, child: Text('Classic')),
                  PopupMenuItem(value: ResumeTemplate.minimal, child: Text('Minimal')),
                ],
                icon: const Icon(Icons.palette_outlined),
              ),
              IconButton(
                tooltip: 'Export PDF',
                onPressed: _exporting ? null : () => _exportPdf(provider.resume),
                icon: _exporting
                    ? const SizedBox(width: 18, height: 18, child: CircularProgressIndicator(strokeWidth: 2))
                    : const Icon(Icons.picture_as_pdf_outlined),
              ),
              const SizedBox(width: 6),
            ],
          ),
          body: ListView(
            padding: const EdgeInsets.fromLTRB(18, 8, 18, 28),
            children: [
              Container(
                padding: const EdgeInsets.all(22),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: const Color(0xFFE4E7EF)),
                  boxShadow: _template == ResumeTemplate.minimal ? [] : const [
                    BoxShadow(color: Color(0x0C202943), blurRadius: 18, offset: Offset(0, 5)),
                  ],
                ),
                child: _ResumeDocument(resume: provider.resume, template: _template),
              ),
              const SizedBox(height: 12),
              Text('$_templateName template · PDF export',
                textAlign: TextAlign.center,
                style: Theme.of(context).textTheme.bodyMedium),
              const SizedBox(height: 8),
              FilledButton.icon(
                onPressed: _exporting ? null : () => _exportPdf(provider.resume),
                icon: const Icon(Icons.download_outlined),
                label: Text(_exporting ? 'Preparing PDF…' : 'Export / Print PDF'),
              ),
              const SizedBox(height: 8),
              const Text(
                'Check dates, contact details and every AI-generated suggestion before sharing your resume.',
                textAlign: TextAlign.center,
                style: TextStyle(fontSize: 12, color: Colors.black54),
              ),
            ],
          ),
        );
      },
    );
  }
}

class _ResumeDocument extends StatelessWidget {
  const _ResumeDocument({required this.resume, required this.template});
  final ResumeModel resume;
  final ResumeTemplate template;

  Color get _accent => switch (template) {
    ResumeTemplate.modern => const Color(0xFF6558D3),
    ResumeTemplate.classic => const Color(0xFF243B53),
    ResumeTemplate.minimal => const Color(0xFF333333),
  };

  @override
  Widget build(BuildContext context) {
    final contact = [resume.email, resume.phone, resume.location]
        .where((value) => value.trim().isNotEmpty).join('  •  ');
    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Text(resume.fullName.isEmpty ? 'Your Name' : resume.fullName,
        style: TextStyle(color: _accent, fontSize: 25, fontWeight: FontWeight.w800)),
      if (resume.targetRole.isNotEmpty) ...[
        const SizedBox(height: 4),
        Text(resume.targetRole, style: TextStyle(color: _accent, fontSize: 15, fontWeight: FontWeight.w700)),
      ],
      if (contact.isNotEmpty) ...[
        const SizedBox(height: 9),
        Text(contact, style: const TextStyle(fontSize: 11, color: Colors.black54)),
      ],
      const SizedBox(height: 17),
      Divider(color: _accent, thickness: 1.2),
      if (resume.professionalSummary.isNotEmpty)
        _PreviewSection(title: 'PROFESSIONAL SUMMARY', body: resume.professionalSummary, accent: _accent),
      for (final entry in resume.effectiveWorkExperiences)
        _PreviewSection(title: 'EXPERIENCE',
          heading: [entry['title'] ?? '', entry['company'] ?? ''].where((v) => v.isNotEmpty).join('  |  '),
          body: [entry['description'] ?? '', [entry['start_date'] ?? '', entry['end_date'] ?? ''].where((v) => v.isNotEmpty).join(' – ')]
              .where((v) => v.isNotEmpty).join('\n'), accent: _accent),
      for (final entry in resume.effectiveEducationEntries)
        _PreviewSection(title: 'EDUCATION',
          heading: [entry['degree'] ?? '', entry['institution'] ?? ''].where((v) => v.isNotEmpty).join('  |  '),
          body: entry['description'] ?? '', accent: _accent),
      for (final entry in resume.projects)
        _PreviewSection(title: 'PROJECT', heading: entry['name'] ?? '',
          body: [entry['description'] ?? '', entry['technologies'] ?? ''].where((v) => v.isNotEmpty).join('\n'), accent: _accent),
      for (final entry in resume.certifications)
        _PreviewSection(title: 'CERTIFICATION', heading: entry['name'] ?? '',
          body: [entry['issuer'] ?? '', entry['date'] ?? ''].where((v) => v.isNotEmpty).join('  |  '), accent: _accent),
      if (resume.skillList.isNotEmpty)
        _PreviewSection(title: 'SKILLS', body: resume.skillList.join('  •  '), accent: _accent),
    ]);
  }
}

class _PreviewSection extends StatelessWidget {
  const _PreviewSection({required this.title, this.heading, required this.body, required this.accent});
  final String title;
  final String? heading;
  final String body;
  final Color accent;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 17),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text(title, style: TextStyle(color: accent, fontSize: 11, fontWeight: FontWeight.w800, letterSpacing: 1)),
        if (heading != null && heading!.isNotEmpty) ...[
          const SizedBox(height: 7),
          Text(heading!, style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w700)),
        ],
        if (body.isNotEmpty) ...[
          const SizedBox(height: 5),
          Text(body, style: const TextStyle(fontSize: 12, height: 1.5, color: Color(0xFF424B5D))),
        ],
      ]),
    );
  }
}
