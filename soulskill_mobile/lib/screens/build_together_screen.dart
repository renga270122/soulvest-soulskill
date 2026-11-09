import 'package:flutter/material.dart';

import '../theme/soulskill_theme.dart';

class BuildTogetherScreen extends StatefulWidget {
  const BuildTogetherScreen({super.key});

  @override
  State<BuildTogetherScreen> createState() => _BuildTogetherScreenState();
}

class _BuildTogetherScreenState extends State<BuildTogetherScreen> {
  final _search = TextEditingController();
  String _interest = 'All interests';
  final List<_Opportunity> _ideas = List.of(_seedIdeas);

  @override
  void dispose() {
    _search.dispose();
    super.dispose();
  }

  Future<void> _shareIdea() async {
    final title = TextEditingController();
    final description = TextEditingController();
    final skills = TextEditingController();
    final result = await showDialog<_Opportunity>(
      context: context,
      builder: (dialogContext) => AlertDialog(
        title: const Text('Share an idea or collaboration request'),
        content: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(controller: title, decoration: const InputDecoration(labelText: 'What would you like to build?')),
              const SizedBox(height: 10),
              TextField(controller: description, maxLines: 3, decoration: const InputDecoration(labelText: 'Describe the problem or opportunity')),
              const SizedBox(height: 10),
              TextField(controller: skills, decoration: const InputDecoration(labelText: 'Skills or collaborators you need')),
            ],
          ),
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(dialogContext), child: const Text('Cancel')),
          FilledButton(
            onPressed: () {
              if (title.text.trim().isEmpty || description.text.trim().isEmpty) return;
              Navigator.pop(dialogContext, _Opportunity(
                title: title.text.trim(),
                description: description.text.trim(),
                skills: skills.text.trim().isEmpty ? 'Open to collaborators' : skills.text.trim(),
                category: 'Community idea',
                members: 'New',
              ));
            },
            child: const Text('Share idea'),
          ),
        ],
      ),
    );
    title.dispose();
    description.dispose();
    skills.dispose();
    if (result != null && mounted) {
      setState(() => _ideas.insert(0, result));
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Added to this preview. Sign-in and community publishing will be connected in a later milestone.')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 3,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('BuildTogether'),
          bottom: const TabBar(
            isScrollable: true,
            tabs: [
              Tab(text: 'Explore'),
              Tab(text: 'Find your people'),
              Tab(text: 'Start consulting'),
            ],
          ),
        ),
        body: TabBarView(
          children: [
            _exploreTab(),
            _peopleTab(),
            _consultingTab(),
          ],
        ),
        floatingActionButton: FloatingActionButton.extended(
          onPressed: _shareIdea,
          icon: const Icon(Icons.add),
          label: const Text('Share an idea'),
        ),
      ),
    );
  }

  Widget _exploreTab() {
    final filtered = _ideas.where((idea) {
      final query = _search.text.toLowerCase();
      final matchesQuery = query.isEmpty ||
          '${idea.title} ${idea.description} ${idea.skills}'.toLowerCase().contains(query);
      final matchesInterest = _interest == 'All interests' || idea.category == _interest;
      return matchesQuery && matchesInterest;
    }).toList();

    return ListView(
      padding: const EdgeInsets.fromLTRB(18, 18, 18, 100),
      children: [
        _introCard(
          eyebrow: 'YOUR NEXT CHAPTER CAN BE BUILT TOGETHER',
          title: 'Your experience is still valuable. What could you create with it?',
          body: 'Explore ideas, meet people with complementary skills, or take the first step toward independent work. There is no pressure to become a founder.',
          icon: Icons.diversity_3_rounded,
        ),
        const SizedBox(height: 20),
        Text('Explore opportunities', style: Theme.of(context).textTheme.titleLarge),
        const SizedBox(height: 10),
        TextField(
          controller: _search,
          onChanged: (_) => setState(() {}),
          decoration: const InputDecoration(
            prefixIcon: Icon(Icons.search),
            hintText: 'Search ideas, skills or problems',
          ),
        ),
        const SizedBox(height: 10),
        DropdownButtonFormField<String>(
          value: _interest,
          decoration: const InputDecoration(labelText: 'Area of interest'),
          items: const [
            'All interests', 'AI & software', 'Consulting', 'Education',
            'Social impact', 'Small business', 'Community idea',
          ].map((value) => DropdownMenuItem(value: value, child: Text(value))).toList(),
          onChanged: (value) => setState(() => _interest = value ?? 'All interests'),
        ),
        const SizedBox(height: 14),
        if (filtered.isEmpty)
          const _EmptyState(message: 'No matching ideas yet. Try another search or share the first idea.')
        else
          ...filtered.map((idea) => Padding(
            padding: const EdgeInsets.only(bottom: 11),
            child: _OpportunityCard(idea: idea),
          )),
        const SizedBox(height: 12),
        const _SafetyNote(
          text: 'Start with a conversation and validate the idea together. Never share passwords, identity documents or money with someone you have not independently verified.',
        ),
      ],
    );
  }

  Widget _peopleTab() {
    return ListView(
      padding: const EdgeInsets.fromLTRB(18, 18, 18, 100),
      children: [
        _introCard(
          eyebrow: 'FIND YOUR PEOPLE',
          title: 'Different skills. Shared ambition.',
          body: 'Connect around interests and complementary strengths. A product idea may need an engineer, a domain expert, a designer and someone who understands customers.',
          icon: Icons.groups_2_rounded,
        ),
        const SizedBox(height: 18),
        Text('Collaboration circles', style: Theme.of(context).textTheme.titleLarge),
        const SizedBox(height: 10),
        const _CircleCard(icon: Icons.auto_awesome, title: 'AI & product builders', detail: 'Explore AI tools, prototypes, automation and practical product ideas.', tags: 'AI · Software · Product'),
        const _CircleCard(icon: Icons.business_center_outlined, title: 'Independent consultants', detail: 'Share expertise, learn how to find clients and explore joint consulting projects.', tags: 'Consulting · B2B · Services'),
        const _CircleCard(icon: Icons.lightbulb_outline, title: 'First-time founders', detail: 'Validate problems, test assumptions and build small experiments together.', tags: 'Startups · MVP · Learning'),
        const _CircleCard(icon: Icons.public, title: 'Purpose-led projects', detail: 'Meet people interested in education, accessibility and community solutions.', tags: 'Social impact · Community'),
        const SizedBox(height: 12),
        const _SafetyNote(text: 'Member discovery, messaging, identity controls and reporting will be enabled with the authenticated community backend. These circles are currently illustrative.'),
      ],
    );
  }

  Widget _consultingTab() {
    return ListView(
      padding: const EdgeInsets.fromLTRB(18, 18, 18, 100),
      children: [
        _introCard(
          eyebrow: 'SOULSKILL EXPERTPRENEUR',
          title: 'Turn what you know into a service someone needs.',
          body: 'Your years of experience can become an independent consulting practice. Start small, test demand and grow at a pace that works for you.',
          icon: Icons.workspace_premium_outlined,
        ),
        const SizedBox(height: 18),
        Text('A practical path to your first client', style: Theme.of(context).textTheme.titleLarge),
        const SizedBox(height: 12),
        const _StepCard(number: '01', title: 'Discover your expertise', body: 'List the problems you have solved, tools you know, industries you understand and outcomes you have delivered.'),
        const _StepCard(number: '02', title: 'Choose a specific customer problem', body: 'Talk to potential customers. Focus on a costly or frustrating problem rather than selling a generic list of skills.'),
        const _StepCard(number: '03', title: 'Package a clear service', body: 'Define the deliverables, timeline, boundaries and a transparent starting price. Avoid promising outcomes you cannot control.'),
        const _StepCard(number: '04', title: 'Build proof and find conversations', body: 'Create a portfolio from work you are allowed to share, ask your network for introductions and offer a small, well-scoped pilot.'),
        const _StepCard(number: '05', title: 'Deliver, learn and repeat', body: 'Use a written scope and agreement, invoice professionally, protect client data and ask for feedback and referrals.'),
        const SizedBox(height: 12),
        _sectionPanel(
          title: 'Consulting profile builder',
          body: 'Prepare these details to shape your first service offer:',
          children: const [
            _ChecklistLine('My strongest 3 areas of expertise'),
            _ChecklistLine('The type of customer I can help'),
            _ChecklistLine('A problem I can solve reliably'),
            _ChecklistLine('A clear deliverable and timeline'),
            _ChecklistLine('A relevant example or portfolio item'),
          ],
        ),
        const SizedBox(height: 12),
        const _SafetyNote(text: 'Before taking paid work, check any applicable employment, confidentiality, intellectual-property, tax and business-registration obligations. Never reuse a former employer’s confidential material.'),
      ],
    );
  }

  Widget _introCard({required String eyebrow, required String title, required String body, required IconData icon}) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: const LinearGradient(colors: [Color(0xFF30226D), Color(0xFF6554D8)]),
        borderRadius: BorderRadius.circular(22),
      ),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Icon(icon, color: const Color(0xFFE5DEFF), size: 29),
        const SizedBox(height: 14),
        Text(eyebrow, style: const TextStyle(color: Color(0xFFD9D1FF), fontSize: 9, fontWeight: FontWeight.w800, letterSpacing: 1)),
        const SizedBox(height: 9),
        Text(title, style: const TextStyle(color: Colors.white, fontSize: 22, height: 1.2, fontWeight: FontWeight.w800)),
        const SizedBox(height: 9),
        Text(body, style: const TextStyle(color: Color(0xFFE9E5FF), fontSize: 12, height: 1.5)),
      ]),
    );
  }

  Widget _sectionPanel({required String title, required String body, required List<Widget> children}) {
    return Container(
      padding: const EdgeInsets.all(17),
      decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(18), border: Border.all(color: SoulSkillTheme.border)),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text(title, style: const TextStyle(fontWeight: FontWeight.w800, color: SoulSkillTheme.ink, fontSize: 15)),
        const SizedBox(height: 5),
        Text(body, style: const TextStyle(color: SoulSkillTheme.muted, fontSize: 12)),
        const SizedBox(height: 12),
        ...children,
      ]),
    );
  }
}

class _Opportunity {
  const _Opportunity({required this.title, required this.description, required this.skills, required this.category, required this.members});
  final String title;
  final String description;
  final String skills;
  final String category;
  final String members;
}

const _seedIdeas = <_Opportunity>[
  _Opportunity(title: 'Build a practical AI workflow for small businesses', description: 'Explore simple ways to reduce repetitive admin work for local service businesses. Start by interviewing a few owners and testing one workflow.', skills: 'AI automation · Operations · Customer discovery', category: 'AI & software', members: 'Idea stage'),
  _Opportunity(title: 'Independent engineering consulting collective', description: 'Bring experienced engineers together to support smaller teams with architecture reviews, testing strategy and delivery coaching.', skills: 'Engineering · Quality · Technical leadership', category: 'Consulting', members: 'Exploring'),
  _Opportunity(title: 'A peer-led career restart circle', description: 'Create a supportive learning group where members share practical job-search lessons and keep each other accountable.', skills: 'Community · Facilitation · Learning', category: 'Community idea', members: 'Idea stage'),
];

class _OpportunityCard extends StatelessWidget {
  const _OpportunityCard({required this.idea});
  final _Opportunity idea;

  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.all(16),
    decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(18), border: Border.all(color: SoulSkillTheme.border)),
    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Row(children: [
        Expanded(child: Text(idea.category.toUpperCase(), style: const TextStyle(color: SoulSkillTheme.violet, fontSize: 9, letterSpacing: .8, fontWeight: FontWeight.w800))),
        Text(idea.members, style: const TextStyle(color: SoulSkillTheme.muted, fontSize: 10)),
      ]),
      const SizedBox(height: 8),
      Text(idea.title, style: const TextStyle(color: SoulSkillTheme.ink, fontSize: 15, fontWeight: FontWeight.w800)),
      const SizedBox(height: 6),
      Text(idea.description, style: const TextStyle(color: SoulSkillTheme.muted, fontSize: 12, height: 1.45)),
      const SizedBox(height: 11),
      Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
        const Icon(Icons.handyman_outlined, size: 15, color: SoulSkillTheme.violet),
        const SizedBox(width: 7),
        Expanded(child: Text(idea.skills, style: const TextStyle(color: SoulSkillTheme.ink, fontSize: 11, fontWeight: FontWeight.w600))),
      ]),
    ]),
  );
}

class _CircleCard extends StatelessWidget {
  const _CircleCard({required this.icon, required this.title, required this.detail, required this.tags});
  final IconData icon;
  final String title;
  final String detail;
  final String tags;

  @override
  Widget build(BuildContext context) => Container(
    margin: const EdgeInsets.only(bottom: 10),
    padding: const EdgeInsets.all(15),
    decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(17), border: Border.all(color: SoulSkillTheme.border)),
    child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Container(width: 40, height: 40, decoration: BoxDecoration(color: const Color(0xFFF0EDFF), borderRadius: BorderRadius.circular(12)), child: Icon(icon, color: SoulSkillTheme.violet)),
      const SizedBox(width: 12),
      Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text(title, style: const TextStyle(color: SoulSkillTheme.ink, fontWeight: FontWeight.w800, fontSize: 13)),
        const SizedBox(height: 4),
        Text(detail, style: const TextStyle(color: SoulSkillTheme.muted, fontSize: 11, height: 1.4)),
        const SizedBox(height: 7),
        Text(tags, style: const TextStyle(color: SoulSkillTheme.violet, fontSize: 10, fontWeight: FontWeight.w700)),
      ])),
    ]),
  );
}

class _StepCard extends StatelessWidget {
  const _StepCard({required this.number, required this.title, required this.body});
  final String number;
  final String title;
  final String body;

  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.only(bottom: 10),
    child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Container(width: 34, height: 34, alignment: Alignment.center, decoration: BoxDecoration(color: const Color(0xFFECEAFF), borderRadius: BorderRadius.circular(11)), child: Text(number, style: const TextStyle(color: SoulSkillTheme.violet, fontWeight: FontWeight.w800, fontSize: 11))),
      const SizedBox(width: 11),
      Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text(title, style: const TextStyle(color: SoulSkillTheme.ink, fontWeight: FontWeight.w800, fontSize: 13)),
        const SizedBox(height: 4),
        Text(body, style: const TextStyle(color: SoulSkillTheme.muted, fontSize: 11, height: 1.45)),
      ])),
    ]),
  );
}

class _ChecklistLine extends StatelessWidget {
  const _ChecklistLine(this.text);
  final String text;
  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.only(bottom: 9),
    child: Row(children: [
      const Icon(Icons.check_circle_outline, color: SoulSkillTheme.violet, size: 17),
      const SizedBox(width: 9),
      Expanded(child: Text(text, style: const TextStyle(color: SoulSkillTheme.ink, fontSize: 12))),
    ]),
  );
}

class _SafetyNote extends StatelessWidget {
  const _SafetyNote({required this.text});
  final String text;
  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.all(13),
    decoration: BoxDecoration(color: const Color(0xFFF5F3FF), borderRadius: BorderRadius.circular(14)),
    child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
      const Icon(Icons.shield_outlined, color: SoulSkillTheme.violet, size: 18),
      const SizedBox(width: 9),
      Expanded(child: Text(text, style: const TextStyle(color: Color(0xFF615985), fontSize: 10.5, height: 1.45))),
    ]),
  );
}

class _EmptyState extends StatelessWidget {
  const _EmptyState({required this.message});
  final String message;
  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.all(22),
    child: Text(message, textAlign: TextAlign.center, style: const TextStyle(color: SoulSkillTheme.muted, fontSize: 12)),
  );
}
