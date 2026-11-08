import 'dart:typed_data';

import 'package:pdf/pdf.dart';
import 'package:pdf/widgets.dart' as pw;

import '../models/resume_model.dart';

class ResumePdfService {
  const ResumePdfService._();

  static Future<Uint8List> create(ResumeModel resume) async {
    final document = pw.Document();
    final contact = [resume.email, resume.phone, resume.location]
        .where((value) => value.trim().isNotEmpty)
        .join(' | ');
    final experienceHeading = [resume.experienceRole, resume.company]
        .where((value) => value.trim().isNotEmpty)
        .join(' | ');
    final educationHeading = [resume.degree, resume.institution]
        .where((value) => value.trim().isNotEmpty)
        .join(' | ');

    document.addPage(
      pw.MultiPage(
        pageFormat: PdfPageFormat.a4,
        margin: const pw.EdgeInsets.fromLTRB(42, 42, 42, 46),
        build: (context) => [
          pw.Text(
            resume.fullName.trim().isEmpty ? 'Your Name' : resume.fullName.trim(),
            style: pw.TextStyle(
              fontSize: 23,
              fontWeight: pw.FontWeight.bold,
              color: PdfColors.blueGrey900,
            ),
          ),
          if (resume.targetRole.trim().isNotEmpty) ...[
            pw.SizedBox(height: 4),
            pw.Text(
              resume.targetRole.trim(),
              style: pw.TextStyle(
                fontSize: 12,
                fontWeight: pw.FontWeight.bold,
                color: PdfColors.deepPurple,
              ),
            ),
          ],
          if (contact.isNotEmpty) ...[
            pw.SizedBox(height: 7),
            pw.Text(contact, style: const pw.TextStyle(fontSize: 9, color: PdfColors.blueGrey700)),
          ],
          pw.SizedBox(height: 13),
          pw.Divider(color: PdfColors.deepPurple300, thickness: 1.2),
          _section('PROFESSIONAL SUMMARY', resume.professionalSummary),
          _section('EXPERIENCE', resume.experienceDescription, heading: experienceHeading),
          _section('EDUCATION', resume.educationDetails, heading: educationHeading),
          _section('SKILLS', resume.skillList.join(', ')),
          if (resume.completionPercent == 0)
            pw.Padding(
              padding: const pw.EdgeInsets.only(top: 18),
              child: pw.Text(
                'Add your information in SoulSkill Resume Studio to build your resume.',
                style: const pw.TextStyle(fontSize: 10, color: PdfColors.grey700),
              ),
            ),
        ],
      ),
    );

    return document.save();
  }

  static pw.Widget _section(String title, String body, {String? heading}) {
    if (body.trim().isEmpty && (heading == null || heading.trim().isEmpty)) {
      return pw.SizedBox.shrink();
    }
    return pw.Padding(
      padding: const pw.EdgeInsets.only(top: 15),
      child: pw.Column(
        crossAxisAlignment: pw.CrossAxisAlignment.start,
        children: [
          pw.Text(
            title,
            style: pw.TextStyle(
              fontSize: 9,
              letterSpacing: 1,
              fontWeight: pw.FontWeight.bold,
              color: PdfColors.deepPurple,
            ),
          ),
          if (heading != null && heading.trim().isNotEmpty) ...[
            pw.SizedBox(height: 6),
            pw.Text(
              heading.trim(),
              style: pw.TextStyle(fontSize: 10, fontWeight: pw.FontWeight.bold, color: PdfColors.blueGrey900),
            ),
          ],
          if (body.trim().isNotEmpty) ...[
            pw.SizedBox(height: 4),
            pw.Text(
              body.trim(),
              style: const pw.TextStyle(fontSize: 9.5, lineSpacing: 3, color: PdfColors.blueGrey800),
            ),
          ],
        ],
      ),
    );
  }
}
