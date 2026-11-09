import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:url_launcher/url_launcher.dart';
import '../models/resume_model.dart';
import '../providers/resume_provider.dart';

class CareerExplorerScreen extends StatelessWidget {
  const CareerExplorerScreen({super.key});

  static const roles = <_Role>[
    _Role('Embedded / Firmware Engineer', ['embedded', 'firmware', 'stm32', 'rtos', 'uart', 'spi', 'device driver', 'iot', 'c++'], 'Firmware, device drivers, microcontrollers and connected products.', ['Bosch', 'Qualcomm', 'NXP', 'Texas Instruments', 'Siemens']),
    _Role('Software Engineer', ['python', 'java', 'javascript', 'typescript', 'flutter', 'react', 'sql', 'api'], 'Application engineering, backend services and product development.', ['TCS', 'Infosys', 'HCLTech', 'Accenture', 'Zoho']),
    _Role('AI / Applied AI Engineer', ['generative ai', 'genai', 'llm', 'machine learning', 'python', 'rag'], 'AI-enabled applications, LLM integrations and workflow automation.', ['Accenture', 'TCS', 'Infosys', 'Freshworks', 'Zoho']),
    _Role('QA / Test Automation Engineer', ['testing', 'automation', 'pytest', 'google test', 'gtest', 'quality assurance', 'python'], 'Test engineering, automation frameworks and product quality.', ['Bosch', 'Qualcomm', 'Siemens', 'HCLTech', 'Accenture']),
    _Role('Cloud / DevOps Engineer', ['aws', 'azure', 'docker', 'kubernetes', 'linux', 'jenkins', 'ci/cd'], 'Cloud platforms, CI/CD, infrastructure and reliability.', ['Amazon', 'Accenture', 'Infosys', 'TCS', 'HCLTech']),
    _Role('Data / Business Analyst', ['sql', 'excel', 'power bi', 'tableau', 'data analysis', 'python'], 'Data reporting, business insights and decision support.', ['Accenture', 'TCS', 'Infosys', 'Freshworks', 'Amazon']),
    _Role('Product / Technical Program Roles', ['leadership', 'stakeholder management', 'agile', 'scrum', 'product management', 'system design'], 'Technical coordination, product delivery and cross-functional execution.', ['Freshworks', 'Zoho', 'Accenture', 'TCS', 'Amazon']),
  ];

  static const companies = <_Company>[
    _Company('Bosch', 'https://www.bosch.in/careers/'),
    _Company('Qualcomm', 'https://www.qualcomm.com/company/careers'),
    _Company('NXP Semiconductors', 'https://www.nxp.com/company/about-nxp/careers:CAREERS'),
    _Company('Texas Instruments', 'https://careers.ti.com/'),
    _Company('Siemens', 'https://www.siemens.com/global/en/company/jobs.html'),
    _Company('TCS', 'https://www.tcs.com/careers'),
    _Company('Infosys', 'https://www.infosys.com/careers/'),
    _Company('HCLTech', 'https://www.hcltech.com/careers'),
    _Company('Accenture', 'https://www.accenture.com/in-en/careers'),
    _Company('Zoho', 'https://www.zoho.com/careers/'),
    _Company('Freshworks', 'https://www.freshworks.com/company/careers/'),
    _Company('Amazon', 'https://www.amazon.jobs/en/'),
  ];

  List<_Role> _recommended(ResumeModel resume) {
    final profile = (resume.targetRole + ' ' + resume.experienceRole + ' ' + resume.experienceDescription + ' ' + resume.skills).toLowerCase();
    final matches = roles.map((role) => (role: role, score: role.keywords.where(profile.contains).length)).where((item) => item.score > 0).toList()
      ..sort((a, b) => b.score.compareTo(a.score));
    if (matches.isNotEmpty) return matches.take(4).map((item) => item.role).toList();
    if (resume.targetRole.trim().isNotEmpty) return [_Role(resume.targetRole.trim(), [], 'Explore openings matching your stated target role.', ['TCS', 'Infosys', 'Accenture', 'HCLTech'])];
    return roles.take(4).toList();
  }

  Future<void> _open(BuildContext context, String url) async {
    final ok = await launchUrl(Uri.parse(url), mode: LaunchMode.externalApplication);
    if (!ok && context.mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Could not open this link.')));
  }

  String _searchUrl(String role, String location) => Uri.https('www.linkedin.com', '/jobs/search/', {'keywords': role, 'location': location}).toString();

  @override
  Widget build(BuildContext context) {
    return Consumer<ResumeProvider>(builder: (context, provider, _) {
      final resume = provider.resume;
      final suggestions = _recommended(resume);
      final companyNames = suggestions.expand((role) => role.companies).toSet();
      final matches = companies.where((company) => companyNames.contains(company.name)).toList();
      final location = resume.location.trim().isEmpty ? 'India' : resume.location.trim();
      return Scaffold(
        appBar: AppBar(title: const Text('Career Explorer')),
        body: ListView(padding: const EdgeInsets.fromLTRB(18, 12, 18, 30), children: [
          Container(padding: const EdgeInsets.all(20), decoration: BoxDecoration(gradient: const LinearGradient(colors: [Color(0xFF30226D), Color(0xFF7359DE)]), borderRadius: BorderRadius.circular(22)), child: const Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Icon(Icons.travel_explore_rounded, color: Colors.white, size: 30),
            SizedBox(height: 12),
            Text('Find roles that fit your skills', style: TextStyle(color: Colors.white, fontSize: 21, fontWeight: FontWeight.w800)),
            SizedBox(height: 7),
            Text('Suggestions use the skills and experience in your saved resume. Explore current openings directly with employers and job boards.', style: TextStyle(color: Color(0xFFEAE5FF), fontSize: 13, height: 1.45)),
          ])),
          if (resume.completionPercent == 0) _notice('Personalize your suggestions', 'Add your skills, experience and target role in Resume Studio. These role paths are a general starting point until your profile is filled in.'),
          _heading('Role paths to explore', 'Based on the resume details saved on this device.'),
          ...suggestions.map((role) => _roleCard(context, role, location)),
          _heading('Companies to keep on your radar', 'Official employer career portals. These are not confirmed vacancies.'),
          ...matches.map((company) => _companyCard(context, company)),
          _notice('About live vacancies', 'Live employer job feeds are not connected yet. Use the links to check current openings, location and eligibility directly.'),
        ]),
      );
    });
  }

  Widget _heading(String title, String subtitle) => Padding(padding: const EdgeInsets.only(top: 18, bottom: 11), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
    Text(title, style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w800, color: Color(0xFF20183D))),
    const SizedBox(height: 4),
    Text(subtitle, style: const TextStyle(fontSize: 12, height: 1.4, color: Color(0xFF706A83))),
  ]));

  Widget _notice(String title, String body) => Container(margin: const EdgeInsets.only(top: 12), padding: const EdgeInsets.all(14), decoration: BoxDecoration(color: const Color(0xFFF4F1FF), borderRadius: BorderRadius.circular(15)), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
    Text(title, style: const TextStyle(fontWeight: FontWeight.w800, color: Color(0xFF5142A0))),
    const SizedBox(height: 4),
    Text(body, style: const TextStyle(fontSize: 12, height: 1.45, color: Color(0xFF655D82))),
  ]));

  Widget _roleCard(BuildContext context, _Role role, String location) => Container(margin: const EdgeInsets.only(bottom: 10), padding: const EdgeInsets.all(15), decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(17), border: Border.all(color: const Color(0xFFEAE6F3))), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
    Row(children: [const Icon(Icons.work_outline_rounded, color: Color(0xFF6842D8)), const SizedBox(width: 9), Expanded(child: Text(role.title, style: const TextStyle(fontWeight: FontWeight.w800, color: Color(0xFF20183D))))]),
    const SizedBox(height: 7),
    Text(role.description, style: const TextStyle(fontSize: 12, height: 1.4, color: Color(0xFF706A83))),
    const SizedBox(height: 10),
    Align(alignment: Alignment.centerRight, child: OutlinedButton.icon(onPressed: () => _open(context, _searchUrl(role.title, location)), icon: const Icon(Icons.search_rounded, size: 17), label: const Text('Find current openings'))),
  ]));

  Widget _companyCard(BuildContext context, _Company company) => Container(margin: const EdgeInsets.only(bottom: 8), padding: const EdgeInsets.symmetric(horizontal: 13, vertical: 9), decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(15), border: Border.all(color: const Color(0xFFEAE6F3))), child: Row(children: [
    const CircleAvatar(radius: 18, backgroundColor: Color(0xFFF0EDFF), child: Icon(Icons.business_rounded, color: Color(0xFF6842D8), size: 19)),
    const SizedBox(width: 11),
    Expanded(child: Text(company.name, style: const TextStyle(fontWeight: FontWeight.w800, color: Color(0xFF20183D)))),
    TextButton(onPressed: () => _open(context, company.url), child: const Text('Careers')),
  ]));
}

class _Role {
  const _Role(this.title, this.keywords, this.description, this.companies);
  final String title;
  final List<String> keywords;
  final String description;
  final List<String> companies;
}

class _Company {
  const _Company(this.name, this.url);
  final String name;
  final String url;
}
