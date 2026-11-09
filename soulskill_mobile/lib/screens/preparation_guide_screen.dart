import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

class PreparationGuideScreen extends StatelessWidget {
  const PreparationGuideScreen({super.key});

  static const resources = <_Resource>[
    _Resource('Resume and job search', 'Build a focused resume, understand job descriptions and organize your search.', [
      _Link('Harvard career resources', 'https://careerservices.fas.harvard.edu/resources/create-a-resume-cv-or-cover-letter/'),
      _Link('LinkedIn Jobs', 'https://www.linkedin.com/jobs/'),
      _Link('Naukri', 'https://www.naukri.com/'),
      _Link('STAR interview method', 'https://www.indeed.com/career-advice/interviewing/how-to-use-the-star-interview-response-technique'),
    ]),
    _Resource('Programming and problem solving', 'Build fundamentals and practise problems progressively in a language relevant to your target role.', [
      _Link('freeCodeCamp', 'https://www.freecodecamp.org/learn/'),
      _Link('HackerRank practice', 'https://www.hackerrank.com/skills-directory'),
      _Link('LeetCode practice', 'https://leetcode.com/problemset/'),
      _Link('Developer roadmaps', 'https://roadmap.sh/'),
    ]),
    _Resource('Embedded systems and firmware', 'Review C/C++, microcontrollers, interfaces, debugging, RTOS and system fundamentals.', [
      _Link('ST learning resources', 'https://www.st.com/content/st_com/en/support/learning.html'),
      _Link('FreeRTOS documentation', 'https://www.freertos.org/Documentation/'),
      _Link('Linux kernel documentation', 'https://docs.kernel.org/'),
      _Link('cppreference', 'https://en.cppreference.com/w/'),
    ]),
    _Resource('AI, machine learning and GenAI', 'Learn ML fundamentals, model evaluation, retrieval, prompt design and safe application integration.', [
      _Link('Google ML Crash Course', 'https://developers.google.com/machine-learning/crash-course'),
      _Link('Hugging Face course', 'https://huggingface.co/learn'),
      _Link('Microsoft Learn AI', 'https://learn.microsoft.com/training/ai/'),
      _Link('OpenAI developer guides', 'https://platform.openai.com/docs/guides'),
    ]),
    _Resource('Cloud and DevOps', 'Practise Linux, version control, CI/CD, containers, cloud fundamentals and deployment workflows.', [
      _Link('AWS Skill Builder', 'https://skillbuilder.aws/'),
      _Link('Microsoft Learn Azure', 'https://learn.microsoft.com/training/azure/'),
      _Link('Docker getting started', 'https://docs.docker.com/get-started/'),
      _Link('GitHub Skills', 'https://skills.github.com/'),
    ]),
    _Resource('Communication and interview readiness', 'Prepare concise examples, explain your decisions and practise role-specific questions.', [
      _Link('MIT career resources', 'https://capd.mit.edu/resources/'),
      _Link('Big Interview articles', 'https://biginterview.com/blog/'),
      _Link('Pramp peer practice', 'https://www.pramp.com/'),
    ]),
  ];

  Future<void> _open(BuildContext context, String url) async {
    final ok = await launchUrl(Uri.parse(url), mode: LaunchMode.externalApplication);
    if (!ok && context.mounted) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Could not open this resource.')));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Preparation Guide')),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(18, 12, 18, 30),
        children: [
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              gradient: const LinearGradient(colors: [Color(0xFF30226D), Color(0xFF7359DE)]),
              borderRadius: BorderRadius.circular(22),
            ),
            child: const Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Icon(Icons.menu_book_rounded, color: Colors.white, size: 30),
              SizedBox(height: 12),
              Text('Prepare with a plan, not pressure.', style: TextStyle(color: Colors.white, fontSize: 21, fontWeight: FontWeight.w800)),
              SizedBox(height: 7),
              Text('A curated starter library of learning materials, practice platforms and interview resources. Check providers for current access terms.', style: TextStyle(color: Color(0xFFEAE5FF), fontSize: 13, height: 1.45)),
            ]),
          ),
          const SizedBox(height: 18),
          ...resources.map((resource) => Container(
            margin: const EdgeInsets.only(bottom: 12),
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(18), border: Border.all(color: const Color(0xFFEAE6F3))),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(resource.title, style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w800, color: Color(0xFF20183D))),
              const SizedBox(height: 5),
              Text(resource.description, style: const TextStyle(fontSize: 12, height: 1.4, color: Color(0xFF706A83))),
              const SizedBox(height: 10),
              ...resource.links.map((link) => ListTile(
                dense: true,
                contentPadding: EdgeInsets.zero,
                leading: const Icon(Icons.open_in_new_rounded, color: Color(0xFF6842D8), size: 18),
                title: Text(link.title, style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w600)),
                trailing: const Icon(Icons.chevron_right_rounded, size: 18),
                onTap: () => _open(context, link.url),
              )),
            ]),
          )),
          const Text('Resource links are provided for learning convenience. Availability, pricing and content may change on provider websites.', style: TextStyle(fontSize: 11, color: Color(0xFF858197), height: 1.4)),
        ],
      ),
    );
  }
}

class _Resource {
  const _Resource(this.title, this.description, this.links);
  final String title;
  final String description;
  final List<_Link> links;
}

class _Link {
  const _Link(this.title, this.url);
  final String title;
  final String url;
}
