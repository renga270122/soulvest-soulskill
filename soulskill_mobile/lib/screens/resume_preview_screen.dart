import 'package:flutter/material.dart';
import 'package:printing/printing.dart';
import 'package:provider/provider.dart';

import '../models/resume_model.dart';
import '../providers/resume_provider.dart';
import '../services/resume_pdf_service.dart';

class ResumePreviewScreen extends StatelessWidget {
  const ResumePreviewScreen({super.key});

  Future<void> _exportPdf(BuildContext context, ResumeModel resume) async {
    try {
      await Printing.layoutPdf(
        onLayout: (format) => ResumePdfService.create(resume),
      );
    } catch (error) {
      if (!context.mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('PDF export failed: ' + error.toString())),
      );
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
              IconButton(
                tooltip: 'Export PDF',
                onPressed: () => _exportPdf(context, provider.resume),
                icon: const Icon(Icons.download_rounded),
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
                ),
                child: _ResumeDocument(resume: provider.resume),
              ),
              const SizedBox(height: 12),
              Text(
                'Review every detail before exporting. This single-column PDF is designed to remain easy to read and parse.',
                textAlign: TextAlign.center,
                style: Theme.of(context).textTheme.bodyMedium,
              ),
            ],
          ),
        );
      },
    );
  }
}

class _ResumeDocument extends StatelessWidget {
  const _ResumeDocument({required this.resume});

  final ResumeModel resume;

  @override
  Widget build(BuildContext context) {
    final contact = [resume.email, resume.phone, resume.location]
        .where((value) => value.trim().isNotEmpty)
        .join('  •  ');

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          resume.fullName.isEmpty ? 'Your Name' : resume.fullName,
          style: const TextStyle(color: Color(0xFF202943), fontSize: 25, fontWeight: FontWeight.w800),
        ),
        if (resume.targetRole.isNotEmpty) ...[
          const SizedBox(height: 4),
          Text(
            resume.targetRole,
            style: const TextStyle(color: Color(0xFF6558D3), fontSize: 15, fontWeight: FontWeight.w700),
          ),
        ],
        if (contact.isNotEmpty) ...[
          const SizedBox(height: 9),
          Text(contact, style: const TextStyle(fontSize: 11, color: Colors.black54)),
        ],
        const SizedBox(height: 17),
        const Divider(color: Color(0xFF6558D3), thickness: 1.2),
        if (resume.professionalSummary.isNotEmpty)
          _PreviewSection(title: 'PROFESSIONAL SUMMARY', body: resume.professionalSummary),
        if (resume.experienceRole.isNotEmpty || resume.company.isNotEmpty || resume.experienceDescription.isNotEmpty)
          _PreviewSection(
            title: 'EXPERIENCE',
            heading: [resume.experienceRole, resume.company].where((value) => value.isNotEmpty).join('  |  '),
            body: resume.experienceDescription,
          ),
        if (resume.degree.isNotEmpty || resume.institution.isNotEmpty || resume.educationDetails.isNotEmpty)
          _PreviewSection(
            title: 'EDUCATION',
            heading: [resume.degree, resume.institution].where((value) => value.isNotEmpty).join('  |  '),
            body: resume.educationDetails,
          ),
        if (resume.skillList.isNotEmpty)
          _PreviewSection(title: 'SKILLS', body: resume.skillList.join('  •  ')),
        if (resume.completionPercent == 0)
          const Padding(
            padding: EdgeInsets.only(top: 18),
            child: Text(
              'Your resume preview will appear here as you add information.',
              style: TextStyle(color: Colors.black54, fontSize: 13),
            ),
          ),
      ],
    );
  }
}

class _PreviewSection extends StatelessWidget {
  const _PreviewSection({required this.title, this.heading, required this.body});

  final String title;
  final String? heading;
  final String body;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 17),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            title,
            style: const TextStyle(color: Color(0xFF6558D3), fontSize: 11, fontWeight: FontWeight.w800, letterSpacing: 1),
          ),
          if (heading != null && heading!.isNotEmpty) ...[
            const SizedBox(height: 7),
            Text(heading!, style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w700)),
          ],
          if (body.isNotEmpty) ...[
            const SizedBox(height: 5),
            Text(body, style: const TextStyle(fontSize: 12, height: 1.5, color: Color(0xFF424B5D))),
          ],
        ],
      ),
    );
  }
}
