import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../providers/resume_provider.dart';
import 'resume_editor_screen.dart';
import 'resume_preview_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  void _openEditor(BuildContext context) {
    Navigator.of(context).push(
      MaterialPageRoute(builder: (_) => const ResumeEditorScreen()),
    );
  }

  void _openPreview(BuildContext context) {
    Navigator.of(context).push(
      MaterialPageRoute(builder: (_) => const ResumePreviewScreen()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<ResumeProvider>(
      builder: (context, provider, _) {
        final progress = provider.resume.completionPercent;

        return Scaffold(
          body: SafeArea(
            child: ListView(
              padding: const EdgeInsets.fromLTRB(20, 14, 20, 30),
              children: [
                Row(
                  children: [
                    Container(
                      width: 42,
                      height: 42,
                      decoration: BoxDecoration(
                        color: const Color(0xFFECEAFF),
                        borderRadius: BorderRadius.circular(14),
                      ),
                      child: const Icon(Icons.auto_awesome_rounded, color: Color(0xFF6558D3), size: 23),
                    ),
                    const SizedBox(width: 11),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('SoulSkill', style: Theme.of(context).textTheme.titleLarge),
                        const Text(
                          'CAREER, WITH CLARITY',
                          style: TextStyle(
                            color: Color(0xFF8991A2),
                            fontSize: 9,
                            fontWeight: FontWeight.w800,
                            letterSpacing: 1.3,
                          ),
                        ),
                      ],
                    ),
                    const Spacer(),
                    IconButton(
                      tooltip: 'Resume editor',
                      onPressed: provider.isLoaded ? () => _openEditor(context) : null,
                      icon: const Icon(Icons.edit_note_rounded),
                    ),
                  ],
                ),
                const SizedBox(height: 28),
                Text('Make your next move\ncount.', style: Theme.of(context).textTheme.headlineMedium),
                const SizedBox(height: 9),
                Text(
                  'Build a clear, confident resume that tells your professional story.',
                  style: Theme.of(context).textTheme.bodyMedium,
                ),
                const SizedBox(height: 22),
                Container(
                  padding: const EdgeInsets.all(21),
                  decoration: BoxDecoration(
                    gradient: const LinearGradient(
                      colors: [Color(0xFF5F53CC), Color(0xFF8979F2)],
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                    ),
                    borderRadius: BorderRadius.circular(24),
                    boxShadow: const [
                      BoxShadow(
                        color: const Color.fromRGBO(101, 88, 211, 0.18),
                        blurRadius: 22,
                        offset: const Offset(0, 10),
                      ),
                    ],
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Row(
                        children: [
                          Expanded(
                            child: Text(
                              'YOUR RESUME WORKSPACE',
                              style: TextStyle(
                                color: Color(0xFFE4E0FF),
                                fontSize: 10,
                                fontWeight: FontWeight.w800,
                                letterSpacing: 1.2,
                              ),
                            ),
                          ),
                          Icon(Icons.description_outlined, color: Colors.white70),
                        ],
                      ),
                      const SizedBox(height: 15),
                      Text(
                        progress == 0 ? 'Start with your story.' : '$progress% complete',
                        style: const TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.w800),
                      ),
                      const SizedBox(height: 7),
                      Text(
                        progress == 0
                            ? 'Add your details and let’s shape your resume together.'
                            : 'Keep going. Every section makes your profile stronger.',
                        style: const TextStyle(color: Color(0xFFEDEBFF), fontSize: 13, height: 1.4),
                      ),
                      const SizedBox(height: 17),
                      ClipRRect(
                        borderRadius: BorderRadius.circular(20),
                        child: LinearProgressIndicator(
                          value: progress / 100,
                          minHeight: 7,
                          backgroundColor: const Color.fromRGBO(255, 255, 255, 0.24),
                          valueColor: const AlwaysStoppedAnimation<Color>(Colors.white),
                        ),
                      ),
                      const SizedBox(height: 18),
                      SizedBox(
                        width: double.infinity,
                        child: FilledButton(
                          onPressed: provider.isLoaded ? () => _openEditor(context) : null,
                          style: FilledButton.styleFrom(
                            backgroundColor: Colors.white,
                            foregroundColor: const Color(0xFF5548BE),
                          ),
                          child: Text(progress == 0 ? 'Start building' : 'Continue editing'),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 27),
                Text('Your next steps', style: Theme.of(context).textTheme.titleLarge),
                const SizedBox(height: 13),
                _ActionTile(
                  icon: Icons.description_outlined,
                  title: 'Build your resume',
                  subtitle: 'Add experience, skills and education',
                  onTap: provider.isLoaded ? () => _openEditor(context) : null,
                ),
                const SizedBox(height: 10),
                _ActionTile(
                  icon: Icons.visibility_outlined,
                  title: 'Preview your resume',
                  subtitle: 'Review how your professional story reads',
                  onTap: progress > 0 ? () => _openPreview(context) : null,
                  muted: progress == 0,
                ),
                const SizedBox(height: 23),
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: const Color(0xFFEFEFFD),
                    borderRadius: BorderRadius.circular(18),
                  ),
                  child: const Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Icon(Icons.lightbulb_outline_rounded, color: Color(0xFF6558D3)),
                      SizedBox(width: 12),
                      Expanded(
                        child: Text(
                          'A good resume is specific, honest and easy to scan. Start with what you have; you can refine it as you go.',
                          style: TextStyle(color: Color(0xFF4F4A7C), fontSize: 12, height: 1.5),
                        ),
                      ),
                    ],
                  ),
                ),
                if (!provider.isLoaded)
                  const Padding(
                    padding: EdgeInsets.only(top: 18),
                    child: Center(child: CircularProgressIndicator()),
                  ),
                if (provider.saveError != null)
                  Padding(
                    padding: const EdgeInsets.only(top: 12),
                    child: Text(provider.saveError!, style: const TextStyle(color: Colors.red, fontSize: 12)),
                  ),
              ],
            ),
          ),
        );
      },
    );
  }
}

class _ActionTile extends StatelessWidget {
  const _ActionTile({
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.onTap,
    this.muted = false,
  });

  final IconData icon;
  final String title;
  final String subtitle;
  final VoidCallback? onTap;
  final bool muted;

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.white,
      borderRadius: BorderRadius.circular(18),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(18),
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 15, vertical: 16),
          child: Row(
            children: [
              Container(
                width: 43,
                height: 43,
                decoration: BoxDecoration(
                  color: muted ? const Color(0xFFF1F2F6) : const Color(0xFFECEAFF),
                  borderRadius: BorderRadius.circular(14),
                ),
                child: Icon(icon, color: muted ? Colors.grey : const Color(0xFF6558D3)),
              ),
              const SizedBox(width: 13),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(title, style: Theme.of(context).textTheme.titleMedium),
                    const SizedBox(height: 3),
                    Text(subtitle, style: Theme.of(context).textTheme.bodyMedium),
                  ],
                ),
              ),
              const Icon(Icons.chevron_right_rounded, color: Color(0xFF9AA2B1)),
            ],
          ),
        ),
      ),
    );
  }
}
