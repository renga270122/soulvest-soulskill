import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../providers/resume_provider.dart';
import '../theme/soulskill_theme.dart';
import 'resume_editor_screen.dart';
import 'resume_preview_screen.dart';

enum _Destination { home, career, coach, soulMind }

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  _Destination _destination = _Destination.home;
  String? _checkIn;

  void _select(_Destination destination) =>
      setState(() => _destination = destination);

  void _openEditor() => Navigator.of(context).push(
        MaterialPageRoute(builder: (_) => const ResumeEditorScreen()),
      );

  void _openPreview() => Navigator.of(context).push(
        MaterialPageRoute(builder: (_) => const ResumePreviewScreen()),
      );

  void _openFeature(String title, String description) {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) =>
            _FeaturePreviewScreen(title: title, description: description),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final wide = MediaQuery.sizeOf(context).width >= 900;

    return Consumer<ResumeProvider>(
      builder: (context, provider, _) {
        final content = _buildDestination(provider);

        if (wide) {
          return Scaffold(
            body: Row(
              children: [
                _DesktopSidebar(
                  selected: _destination,
                  onSelected: _select,
                  onOpenProfile: () => _openFeature(
                    'Your career profile',
                    'Your profile will become the reusable source of truth for resumes, job applications and admissions documents.',
                  ),
                ),
                Expanded(
                  child: Column(
                    children: [
                      _DesktopTopBar(
                        saveError: provider.saveError,
                        isSaving: provider.isSaving,
                      ),
                      Expanded(
                        child: Center(
                          child: ConstrainedBox(
                            constraints: const BoxConstraints(maxWidth: 1240),
                            child: content,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          );
        }

        return Scaffold(
          appBar: _MobileTopBar(
            onProfileTap: () => _openFeature(
              'Your career profile',
              'Your profile will become the reusable source of truth for resumes, job applications and admissions documents.',
            ),
          ),
          body: content,
          bottomNavigationBar: NavigationBar(
            selectedIndex: _destination.index,
            onDestinationSelected: (index) =>
                _select(_Destination.values[index]),
            destinations: const [
              NavigationDestination(
                icon: Icon(Icons.home_outlined),
                selectedIcon: Icon(Icons.home_rounded),
                label: 'Home',
              ),
              NavigationDestination(
                icon: Icon(Icons.description_outlined),
                selectedIcon: Icon(Icons.description_rounded),
                label: 'Career',
              ),
              NavigationDestination(
                icon: Icon(Icons.psychology_alt_outlined),
                selectedIcon: Icon(Icons.psychology_alt_rounded),
                label: 'Coach',
              ),
              NavigationDestination(
                icon: Icon(Icons.favorite_border_rounded),
                selectedIcon: Icon(Icons.favorite_rounded),
                label: 'SoulMind',
              ),
            ],
          ),
        );
      },
    );
  }

  Widget _buildDestination(ResumeProvider provider) {
    switch (_destination) {
      case _Destination.home:
        return _DashboardView(
          progress: provider.resume.completionPercent,
          isLoaded: provider.isLoaded,
          onCreateResume: _openEditor,
          onOpenCareer: () => _select(_Destination.career),
          onOpenCoach: () => _select(_Destination.coach),
          onOpenSoulMind: () => _select(_Destination.soulMind),
          onOpenFeature: _openFeature,
          onOpenPreview:
              provider.resume.completionPercent > 0 ? _openPreview : null,
          checkIn: _checkIn,
          onCheckIn: (value) {
            setState(() {
              _checkIn = value;
              _destination = _Destination.soulMind;
            });
          },
        );
      case _Destination.career:
        return _CareerStudioView(
          progress: provider.resume.completionPercent,
          onCreateResume: _openEditor,
          onPreview:
              provider.resume.completionPercent > 0 ? _openPreview : null,
          onOpenFeature: _openFeature,
        );
      case _Destination.coach:
        return _SoulCoachView(onOpenFeature: _openFeature);
      case _Destination.soulMind:
        return _SoulMindView(
          checkIn: _checkIn,
          onClearCheckIn: () => setState(() => _checkIn = null),
        );
    }
  }
}

class _MobileTopBar extends StatelessWidget implements PreferredSizeWidget {
  const _MobileTopBar({required this.onProfileTap});

  final VoidCallback onProfileTap;

  @override
  Size get preferredSize => const Size.fromHeight(68);

  @override
  Widget build(BuildContext context) {
    return AppBar(
      automaticallyImplyLeading: false,
      titleSpacing: 18,
      title: const _BrandLockup(compact: true),
      actions: [
        IconButton(
          tooltip: 'Your profile',
          onPressed: onProfileTap,
          icon: const CircleAvatar(
            radius: 16,
            backgroundColor: Color(0xFFECEAFF),
            child: Icon(Icons.person_outline_rounded,
                color: SoulSkillTheme.violet, size: 19),
          ),
        ),
        const SizedBox(width: 8),
      ],
    );
  }
}

class _DesktopTopBar extends StatelessWidget {
  const _DesktopTopBar({required this.saveError, required this.isSaving});

  final String? saveError;
  final bool isSaving;

  @override
  Widget build(BuildContext context) {
    final status =
        saveError ?? (isSaving ? 'Saving draft…' : 'Your career workspace');

    return Container(
      height: 76,
      padding: const EdgeInsets.symmetric(horizontal: 30),
      decoration: const BoxDecoration(
        color: Colors.white,
        border: Border(bottom: BorderSide(color: SoulSkillTheme.border)),
      ),
      child: Row(
        children: [
          Expanded(
            child: Text(
              'A clearer path to your next opportunity',
              style: Theme.of(context).textTheme.titleMedium,
            ),
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 9),
            decoration: BoxDecoration(
              color: const Color(0xFFF5F3FF),
              borderRadius: BorderRadius.circular(30),
            ),
            child: Row(
              children: [
                Icon(
                  saveError != null
                      ? Icons.info_outline_rounded
                      : Icons.cloud_done_outlined,
                  size: 16,
                  color: saveError != null
                      ? Colors.orange.shade800
                      : SoulSkillTheme.violet,
                ),
                const SizedBox(width: 7),
                Text(
                  status,
                  style: const TextStyle(
                    color: SoulSkillTheme.muted,
                    fontSize: 12,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(width: 14),
          const Icon(Icons.language_rounded,
              color: SoulSkillTheme.muted, size: 21),
        ],
      ),
    );
  }
}

class _BrandLockup extends StatelessWidget {
  const _BrandLockup({this.compact = false});

  final bool compact;

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: compact ? 38 : 42,
          height: compact ? 38 : 42,
          decoration: BoxDecoration(
            color: const Color(0xFFECEAFF),
            borderRadius: BorderRadius.circular(13),
          ),
          child: const Icon(Icons.auto_awesome_rounded,
              color: SoulSkillTheme.violet, size: 22),
        ),
        const SizedBox(width: 10),
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              'SoulSkill',
              style: TextStyle(
                color: SoulSkillTheme.ink,
                fontSize: compact ? 18 : 20,
                fontWeight: FontWeight.w800,
                letterSpacing: -0.45,
              ),
            ),
            if (!compact)
              const Text(
                'CAREER, WITH CLARITY',
                style: TextStyle(
                  color: SoulSkillTheme.muted,
                  fontSize: 9,
                  fontWeight: FontWeight.w800,
                  letterSpacing: 1.15,
                ),
              ),
          ],
        ),
      ],
    );
  }
}

class _DesktopSidebar extends StatelessWidget {
  const _DesktopSidebar({
    required this.selected,
    required this.onSelected,
    required this.onOpenProfile,
  });

  final _Destination selected;
  final ValueChanged<_Destination> onSelected;
  final VoidCallback onOpenProfile;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 270,
      padding: const EdgeInsets.fromLTRB(17, 24, 15, 18),
      decoration: const BoxDecoration(
        color: Colors.white,
        border: Border(right: BorderSide(color: SoulSkillTheme.border)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Padding(
            padding: EdgeInsets.only(left: 8, bottom: 32),
            child: _BrandLockup(compact: true),
          ),
          const _SidebarLabel('WORKSPACE'),
          _SidebarItem(
            icon: Icons.home_outlined,
            label: 'Home',
            selected: selected == _Destination.home,
            onTap: () => onSelected(_Destination.home),
          ),
          _SidebarItem(
            icon: Icons.description_outlined,
            label: 'Career Studio',
            selected: selected == _Destination.career,
            onTap: () => onSelected(_Destination.career),
          ),
          _SidebarItem(
            icon: Icons.psychology_alt_outlined,
            label: 'SoulCoach',
            selected: selected == _Destination.coach,
            onTap: () => onSelected(_Destination.coach),
          ),
          _SidebarItem(
            icon: Icons.favorite_border_rounded,
            label: 'SoulMind',
            selected: selected == _Destination.soulMind,
            onTap: () => onSelected(_Destination.soulMind),
          ),
          const SizedBox(height: 25),
          const _SidebarLabel('EXPLORE'),
          const _SidebarItem(
            icon: Icons.track_changes_outlined,
            label: 'Job matching',
            selected: false,
            onTap: null,
            badge: 'NEXT',
          ),
          const _SidebarItem(
            icon: Icons.school_outlined,
            label: 'Admissions',
            selected: false,
            onTap: null,
            badge: 'NEXT',
          ),
          const Spacer(),
          Container(
            padding: const EdgeInsets.all(13),
            decoration: BoxDecoration(
              color: const Color(0xFFF5F3FF),
              borderRadius: BorderRadius.circular(15),
            ),
            child: const Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Icon(Icons.lightbulb_outline_rounded,
                    color: SoulSkillTheme.violet, size: 19),
                SizedBox(width: 9),
                Expanded(
                  child: Text(
                    'Small, consistent steps can move your career forward.',
                    style: TextStyle(
                      color: Color(0xFF635A92),
                      fontSize: 11,
                      height: 1.45,
                    ),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 13),
          InkWell(
            onTap: onOpenProfile,
            borderRadius: BorderRadius.circular(12),
            child: const Padding(
              padding: EdgeInsets.symmetric(horizontal: 9, vertical: 10),
              child: Row(
                children: [
                  CircleAvatar(
                    radius: 17,
                    backgroundColor: Color(0xFFECEAFF),
                    child: Icon(Icons.person_outline,
                        color: SoulSkillTheme.violet, size: 19),
                  ),
                  SizedBox(width: 10),
                  Expanded(
                    child: Text(
                      'My profile',
                      style: TextStyle(
                        color: SoulSkillTheme.ink,
                        fontWeight: FontWeight.w700,
                        fontSize: 13,
                      ),
                    ),
                  ),
                  Icon(Icons.chevron_right,
                      color: SoulSkillTheme.muted, size: 19),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _SidebarLabel extends StatelessWidget {
  const _SidebarLabel(this.label);

  final String label;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(10, 0, 0, 10),
      child: Text(
        label,
        style: const TextStyle(
          color: Color(0xFF9AA2B1),
          fontSize: 10,
          fontWeight: FontWeight.w800,
          letterSpacing: 1.15,
        ),
      ),
    );
  }
}

class _SidebarItem extends StatelessWidget {
  const _SidebarItem({
    required this.icon,
    required this.label,
    required this.selected,
    required this.onTap,
    this.badge,
  });

  final IconData icon;
  final String label;
  final bool selected;
  final VoidCallback? onTap;
  final String? badge;

  @override
  Widget build(BuildContext context) {
    final color =
        onTap == null ? const Color(0xFFA7ADBA) : selected
            ? SoulSkillTheme.violet
            : SoulSkillTheme.muted;
    return Padding(
      padding: const EdgeInsets.only(bottom: 5),
      child: Material(
        color: selected ? const Color(0xFFF0EDFF) : Colors.transparent,
        borderRadius: BorderRadius.circular(12),
        child: InkWell(
          onTap: onTap,
          borderRadius: BorderRadius.circular(12),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 11, vertical: 12),
            child: Row(
              children: [
                Icon(icon, color: color, size: 19),
                const SizedBox(width: 11),
                Expanded(
                  child: Text(
                    label,
                    style: TextStyle(
                      color: color,
                      fontSize: 12.5,
                      fontWeight:
                          selected ? FontWeight.w800 : FontWeight.w600,
                    ),
                  ),
                ),
                if (badge != null)
                  Text(
                    badge!,
                    style: const TextStyle(
                      color: Color(0xFF9AA2B1),
                      fontSize: 8,
                      fontWeight: FontWeight.w800,
                      letterSpacing: 0.4,
                    ),
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _DashboardView extends StatelessWidget {
  const _DashboardView({
    required this.progress,
    required this.isLoaded,
    required this.onCreateResume,
    required this.onOpenCareer,
    required this.onOpenCoach,
    required this.onOpenSoulMind,
    required this.onOpenFeature,
    required this.onOpenPreview,
    required this.checkIn,
    required this.onCheckIn,
  });

  final int progress;
  final bool isLoaded;
  final VoidCallback onCreateResume;
  final VoidCallback onOpenCareer;
  final VoidCallback onOpenCoach;
  final VoidCallback onOpenSoulMind;
  final void Function(String, String) onOpenFeature;
  final VoidCallback? onOpenPreview;
  final String? checkIn;
  final ValueChanged<String> onCheckIn;

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        final wide = constraints.maxWidth >= 820;
        final sideBySide = constraints.maxWidth >= 1050;

        return ListView(
          padding: EdgeInsets.fromLTRB(
            wide ? 30 : 18,
            wide ? 27 : 20,
            wide ? 30 : 18,
            34,
          ),
          children: [
            _WelcomeHeader(wide: wide),
            const SizedBox(height: 20),
            _HeroPanel(
              onCreateResume: onCreateResume,
              onOpenSoulMind: onOpenSoulMind,
              wide: wide,
            ),
            const SizedBox(height: 18),
            _ProgressSummary(
              progress: progress,
              isLoaded: isLoaded,
              onTap: onOpenCareer,
              wide: wide,
            ),
            const SizedBox(height: 28),
            const _SectionHeading(
              title: 'Your career workspace',
              subtitle: 'Everything you need, in one place.',
              trailing: 'Explore',
            ),
            const SizedBox(height: 14),
            _QuickActionGrid(
              wide: wide,
              onCareer: onOpenCareer,
              onCoach: onOpenCoach,
              onSoulMind: onOpenSoulMind,
              onFeature: onOpenFeature,
            ),
            const SizedBox(height: 28),
            if (sideBySide)
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Expanded(
                    flex: 6,
                    child: _NextStepCard(
                      progress: progress,
                      onContinue: onCreateResume,
                      onPreview: onOpenPreview,
                    ),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    flex: 5,
                    child: _EncouragementCard(
                      checkIn: checkIn,
                      onCheckIn: onCheckIn,
                      onOpenSoulMind: onOpenSoulMind,
                    ),
                  ),
                ],
              )
            else ...[
              _NextStepCard(
                progress: progress,
                onContinue: onCreateResume,
                onPreview: onOpenPreview,
              ),
              const SizedBox(height: 14),
              _EncouragementCard(
                checkIn: checkIn,
                onCheckIn: onCheckIn,
                onOpenSoulMind: onOpenSoulMind,
              ),
            ],
            const SizedBox(height: 24),
            _TrustNote(
              onTap: () => onOpenFeature(
                'Your information stays yours',
                'SoulSkill is being built around private-by-default career profiles. Cloud accounts, sharing permissions and data export controls will be introduced before public release.',
              ),
            ),
          ],
        );
      },
    );
  }
}

class _WelcomeHeader extends StatelessWidget {
  const _WelcomeHeader({required this.wide});

  final bool wide;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Welcome to your next chapter',
                style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                      fontSize: wide ? 26 : 23,
                    ),
              ),
              const SizedBox(height: 5),
              Text(
                'Build your skills, tell your story and move forward with confidence.',
                style: Theme.of(context).textTheme.bodyMedium,
              ),
            ],
          ),
        ),
        if (wide)
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(30),
              border: Border.all(color: SoulSkillTheme.border),
            ),
            child: const Row(
              children: [
                Icon(Icons.public_rounded,
                    color: SoulSkillTheme.violet, size: 16),
                SizedBox(width: 7),
                Text(
                  'A global career workspace',
                  style: TextStyle(
                    color: SoulSkillTheme.muted,
                    fontSize: 11,
                    fontWeight: FontWeight.w700,
                  ),
                ),
              ],
            ),
          ),
      ],
    );
  }
}

class _HeroPanel extends StatelessWidget {
  const _HeroPanel({
    required this.onCreateResume,
    required this.onOpenSoulMind,
    required this.wide,
  });

  final VoidCallback onCreateResume;
  final VoidCallback onOpenSoulMind;
  final bool wide;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(wide ? 26 : 21),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [Color(0xFF30226D), Color(0xFF6554D8), Color(0xFF8879F0)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(24),
        boxShadow: const [
          BoxShadow(
            color: Color(0x1F5646C5),
            blurRadius: 26,
            offset: Offset(0, 12),
          ),
        ],
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Expanded(
            flex: 7,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                  decoration: BoxDecoration(
                    color: Colors.white.withValues(alpha: 0.13),
                    borderRadius: BorderRadius.circular(30),
                    border: Border.all(
                      color: Colors.white.withValues(alpha: 0.18),
                    ),
                  ),
                  child: const Text(
                    'YOUR AI CAREER COMPANION',
                    style: TextStyle(
                      color: Color(0xFFE9E4FF),
                      fontSize: 9,
                      letterSpacing: 1.1,
                      fontWeight: FontWeight.w800,
                    ),
                  ),
                ),
                const SizedBox(height: 17),
                Text(
                  wide
                      ? 'Your next opportunity starts with a stronger story.'
                      : 'Build a career story that moves you forward.',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: wide ? 27 : 23,
                    height: 1.12,
                    fontWeight: FontWeight.w800,
                    letterSpacing: -0.65,
                  ),
                ),
                const SizedBox(height: 10),
                const Text(
                  'Create a thoughtful resume, prepare for opportunities and keep your confidence along the way.',
                  style: TextStyle(
                    color: Color(0xFFE9E5FF),
                    fontSize: 12.5,
                    height: 1.5,
                  ),
                ),
                const SizedBox(height: 19),
                Wrap(
                  spacing: 9,
                  runSpacing: 9,
                  children: [
                    FilledButton.icon(
                      onPressed: onCreateResume,
                      style: FilledButton.styleFrom(
                        backgroundColor: Colors.white,
                        foregroundColor: const Color(0xFF4F42B5),
                        padding: const EdgeInsets.symmetric(
                            horizontal: 15, vertical: 13),
                      ),
                      icon: const Icon(Icons.edit_note_rounded, size: 17),
                      label: const Text('Create / improve resume'),
                    ),
                    OutlinedButton.icon(
                      onPressed: onOpenSoulMind,
                      style: OutlinedButton.styleFrom(
                        foregroundColor: Colors.white,
                        side: BorderSide(
                            color: Colors.white.withValues(alpha: 0.45)),
                        padding: const EdgeInsets.symmetric(
                            horizontal: 14, vertical: 13),
                      ),
                      icon: const Icon(Icons.favorite_border, size: 17),
                      label: const Text('Take a mindful pause'),
                    ),
                  ],
                ),
              ],
            ),
          ),
          if (wide) ...[
            const SizedBox(width: 18),
            Container(
              width: 148,
              height: 148,
              decoration: BoxDecoration(
                color: Colors.white.withValues(alpha: 0.10),
                shape: BoxShape.circle,
                border: Border.all(
                    color: Colors.white.withValues(alpha: 0.18), width: 1.4),
              ),
              child: const Icon(Icons.spa_rounded,
                  color: Color(0xFFE9DFFF), size: 83),
            ),
          ],
        ],
      ),
    );
  }
}

class _ProgressSummary extends StatelessWidget {
  const _ProgressSummary({
    required this.progress,
    required this.isLoaded,
    required this.onTap,
    required this.wide,
  });

  final int progress;
  final bool isLoaded;
  final VoidCallback onTap;
  final bool wide;

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(18),
      child: Container(
        padding: const EdgeInsets.all(17),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(18),
          border: Border.all(color: SoulSkillTheme.border),
        ),
        child: Row(
          children: [
            SizedBox(
              width: 54,
              height: 54,
              child: Stack(
                fit: StackFit.expand,
                children: [
                  CircularProgressIndicator(
                    value: isLoaded ? progress / 100 : null,
                    strokeWidth: 5,
                    backgroundColor: const Color(0xFFECEAFF),
                    valueColor: const AlwaysStoppedAnimation(
                        SoulSkillTheme.violet),
                  ),
                  Center(
                    child: Text(
                      isLoaded ? '$progress%' : '…',
                      style: const TextStyle(
                        color: SoulSkillTheme.ink,
                        fontSize: 12,
                        fontWeight: FontWeight.w800,
                      ),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(width: 15),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Your resume progress',
                    style: TextStyle(
                      color: SoulSkillTheme.ink,
                      fontWeight: FontWeight.w800,
                      fontSize: 14,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    isLoaded
                        ? progress == 0
                            ? 'Start with the details you already have.'
                            : progress == 100
                                ? 'Your current draft is complete. Review it before sharing.'
                                : 'You are building your professional story. Keep going.'
                        : 'Loading your saved draft…',
                    style: Theme.of(context).textTheme.bodyMedium,
                  ),
                ],
              ),
            ),
            if (wide)
              const Icon(Icons.arrow_forward_rounded,
                  color: SoulSkillTheme.violet, size: 20),
          ],
        ),
      ),
    );
  }
}

class _SectionHeading extends StatelessWidget {
  const _SectionHeading({
    required this.title,
    required this.subtitle,
    this.trailing,
  });

  final String title;
  final String subtitle;
  final String? trailing;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(title, style: Theme.of(context).textTheme.titleLarge),
              const SizedBox(height: 3),
              Text(subtitle, style: Theme.of(context).textTheme.bodyMedium),
            ],
          ),
        ),
        if (trailing != null)
          Text(
            trailing!,
            style: const TextStyle(
              color: SoulSkillTheme.violet,
              fontSize: 11,
              fontWeight: FontWeight.w800,
            ),
          ),
      ],
    );
  }
}

class _QuickActionGrid extends StatelessWidget {
  const _QuickActionGrid({
    required this.wide,
    required this.onCareer,
    required this.onCoach,
    required this.onSoulMind,
    required this.onFeature,
  });

  final bool wide;
  final VoidCallback onCareer;
  final VoidCallback onCoach;
  final VoidCallback onSoulMind;
  final void Function(String, String) onFeature;

  @override
  Widget build(BuildContext context) {
    final items = <_ActionData>[
      _ActionData(
        icon: Icons.description_outlined,
        title: 'Resume Studio',
        subtitle: 'Build and refine your resume',
        color: const Color(0xFF6558D3),
        onTap: onCareer,
      ),
      _ActionData(
        icon: Icons.track_changes_outlined,
        title: 'Job matching',
        subtitle: 'Understand role requirements',
        color: const Color(0xFF238A81),
        status: 'NEXT',
        onTap: () => onFeature(
          'Job matching & ATS insights',
          'Compare a resume with a job description, understand skill evidence and discover practical improvements. This capability is planned for the next product milestone.',
        ),
      ),
      _ActionData(
        icon: Icons.mic_none_rounded,
        title: 'Interview practice',
        subtitle: 'Prepare with confidence',
        color: const Color(0xFFD47A4B),
        status: 'NEXT',
        onTap: () => onFeature(
          'Interview practice',
          'Practice role-specific questions, structure your answers and receive useful feedback. The interview coach is planned for a later milestone.',
        ),
      ),
      _ActionData(
        icon: Icons.school_outlined,
        title: 'Admissions',
        subtitle: 'Academic CV and SOP support',
        color: const Color(0xFF5275C8),
        status: 'NEXT',
        onTap: () => onFeature(
          'Admissions Studio',
          'Prepare an academic CV, organize program requirements and develop an authentic statement of purpose. Admissions tools are planned after the core career experience.',
        ),
      ),
      _ActionData(
        icon: Icons.favorite_border_rounded,
        title: 'SoulMind',
        subtitle: 'Affirmations and reflection',
        color: const Color(0xFFB65C88),
        onTap: onSoulMind,
      ),
      _ActionData(
        icon: Icons.checklist_rounded,
        title: 'Applications',
        subtitle: 'Keep your next steps organized',
        color: const Color(0xFF6B8E63),
        status: 'NEXT',
        onTap: () => onFeature(
          'Application tracker',
          'Keep roles, application stages and follow-up dates in one place. The tracker is planned for a future release.',
        ),
      ),
    ];

    return GridView.builder(
      itemCount: items.length,
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: wide ? 3 : 2,
        crossAxisSpacing: 11,
        mainAxisSpacing: 11,
        mainAxisExtent: wide ? 132 : 138,
      ),
      itemBuilder: (context, index) => _ActionCard(item: items[index]),
    );
  }
}

class _ActionData {
  const _ActionData({
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.color,
    required this.onTap,
    this.status,
  });

  final IconData icon;
  final String title;
  final String subtitle;
  final Color color;
  final VoidCallback onTap;
  final String? status;
}

class _ActionCard extends StatelessWidget {
  const _ActionCard({required this.item});

  final _ActionData item;

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.white,
      borderRadius: BorderRadius.circular(17),
      child: InkWell(
        onTap: item.onTap,
        borderRadius: BorderRadius.circular(17),
        child: Container(
          padding: const EdgeInsets.all(14),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(17),
            border: Border.all(color: SoulSkillTheme.border),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Container(
                    width: 37,
                    height: 37,
                    decoration: BoxDecoration(
                      color: item.color.withValues(alpha: 0.10),
                      borderRadius: BorderRadius.circular(11),
                    ),
                    child: Icon(item.icon, color: item.color, size: 20),
                  ),
                  const Spacer(),
                  if (item.status != null)
                    Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 6, vertical: 4),
                      decoration: BoxDecoration(
                        color: const Color(0xFFF3F4F7),
                        borderRadius: BorderRadius.circular(20),
                      ),
                      child: Text(
                        item.status!,
                        style: const TextStyle(
                          color: SoulSkillTheme.muted,
                          fontSize: 8,
                          fontWeight: FontWeight.w800,
                          letterSpacing: 0.4,
                        ),
                      ),
                    )
                  else
                    const Icon(Icons.arrow_outward_rounded,
                        color: Color(0xFF9AA2B1), size: 16),
                ],
              ),
              const Spacer(),
              Text(
                item.title,
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
                style: const TextStyle(
                  color: SoulSkillTheme.ink,
                  fontSize: 13,
                  fontWeight: FontWeight.w800,
                ),
              ),
              const SizedBox(height: 3),
              Text(
                item.subtitle,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
                style: const TextStyle(
                  color: SoulSkillTheme.muted,
                  fontSize: 10.5,
                  height: 1.3,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _NextStepCard extends StatelessWidget {
  const _NextStepCard({
    required this.progress,
    required this.onContinue,
    required this.onPreview,
  });

  final int progress;
  final VoidCallback onContinue;
  final VoidCallback? onPreview;

  @override
  Widget build(BuildContext context) {
    final title = progress == 0
        ? 'Start with your profile'
        : progress >= 100
            ? 'Review your resume'
            : 'Add the next important detail';
    final description = progress == 0
        ? 'Add your contact details, target role and a short introduction. You can refine everything later.'
        : progress >= 100
            ? 'Check the wording and make sure every detail accurately reflects your experience.'
            : 'Add relevant experience, education and skills so your resume represents you more completely.';

    return _SurfaceCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const _Eyebrow(icon: Icons.flag_outlined, label: 'YOUR NEXT STEP'),
          const SizedBox(height: 13),
          Text(title, style: Theme.of(context).textTheme.titleLarge),
          const SizedBox(height: 6),
          Text(description, style: Theme.of(context).textTheme.bodyMedium),
          const SizedBox(height: 16),
          Row(
            children: [
              Expanded(
                child: FilledButton(
                  onPressed: onContinue,
                  child: Text(
                    progress >= 100
                        ? 'Continue to Career Studio'
                        : 'Continue building',
                  ),
                ),
              ),
              if (onPreview != null) ...[
                const SizedBox(width: 8),
                IconButton.filledTonal(
                  tooltip: 'Preview resume',
                  onPressed: onPreview,
                  icon: const Icon(Icons.visibility_outlined),
                ),
              ],
            ],
          ),
        ],
      ),
    );
  }
}

class _EncouragementCard extends StatelessWidget {
  const _EncouragementCard({
    required this.checkIn,
    required this.onCheckIn,
    required this.onOpenSoulMind,
  });

  final String? checkIn;
  final ValueChanged<String> onCheckIn;
  final VoidCallback onOpenSoulMind;

  @override
  Widget build(BuildContext context) {
    return _SurfaceCard(
      color: const Color(0xFFF3F0FF),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const _Eyebrow(
            icon: Icons.wb_twilight_rounded,
            label: 'A MOMENT FOR YOU',
            color: Color(0xFF6558D3),
          ),
          const SizedBox(height: 13),
          const Text(
            'Your worth is bigger than a job title.',
            style: TextStyle(
              color: SoulSkillTheme.ink,
              fontSize: 18,
              height: 1.2,
              fontWeight: FontWeight.w800,
              letterSpacing: -0.3,
            ),
          ),
          const SizedBox(height: 7),
          const Text(
            'Take your career one step at a time. You can build confidence while you build your next opportunity.',
            style: TextStyle(
              color: Color(0xFF6E6792),
              fontSize: 12,
              height: 1.45,
            ),
          ),
          const SizedBox(height: 15),
          const Text(
            'How are you feeling about your career journey today?',
            style: TextStyle(
              color: SoulSkillTheme.ink,
              fontSize: 11,
              fontWeight: FontWeight.w800,
            ),
          ),
          const SizedBox(height: 9),
          Wrap(
            spacing: 7,
            runSpacing: 7,
            children: [
              _CheckInChip(
                label: 'Motivated',
                selected: checkIn == 'Motivated',
                onTap: () => onCheckIn('Motivated'),
              ),
              _CheckInChip(
                label: 'Unsure',
                selected: checkIn == 'Unsure',
                onTap: () => onCheckIn('Unsure'),
              ),
              _CheckInChip(
                label: 'Need a reset',
                selected: checkIn == 'Need a reset',
                onTap: () => onCheckIn('Need a reset'),
              ),
            ],
          ),
          const SizedBox(height: 11),
          TextButton.icon(
            onPressed: onOpenSoulMind,
            style: TextButton.styleFrom(
              padding: EdgeInsets.zero,
              foregroundColor: SoulSkillTheme.violet,
            ),
            icon: const Icon(Icons.favorite_border, size: 16),
            label: const Text('Open SoulMind'),
          ),
        ],
      ),
    );
  }
}

class _CheckInChip extends StatelessWidget {
  const _CheckInChip({
    required this.label,
    required this.selected,
    required this.onTap,
  });

  final String label;
  final bool selected;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return ChoiceChip(
      label: Text(label),
      selected: selected,
      onSelected: (_) => onTap(),
      labelStyle: TextStyle(
        color: selected ? Colors.white : const Color(0xFF655C8F),
        fontSize: 10,
        fontWeight: FontWeight.w700,
      ),
      selectedColor: SoulSkillTheme.violet,
      backgroundColor: Colors.white.withValues(alpha: 0.75),
      side: BorderSide(
        color: selected ? SoulSkillTheme.violet : const Color(0xFFE2DDF5),
      ),
      visualDensity: VisualDensity.compact,
      padding: const EdgeInsets.symmetric(horizontal: 5),
    );
  }
}

class _TrustNote extends StatelessWidget {
  const _TrustNote({required this.onTap});

  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(14),
      child: const Padding(
        padding: EdgeInsets.symmetric(vertical: 8),
        child: Row(
          children: [
            Icon(Icons.shield_outlined,
                color: SoulSkillTheme.muted, size: 17),
            SizedBox(width: 8),
            Expanded(
              child: Text(
                'Your career story belongs to you. Review every AI suggestion before using it.',
                style: TextStyle(
                  color: SoulSkillTheme.muted,
                  fontSize: 10.5,
                  height: 1.4,
                ),
              ),
            ),
            Icon(Icons.chevron_right,
                color: SoulSkillTheme.muted, size: 17),
          ],
        ),
      ),
    );
  }
}

class _CareerStudioView extends StatelessWidget {
  const _CareerStudioView({
    required this.progress,
    required this.onCreateResume,
    required this.onPreview,
    required this.onOpenFeature,
  });

  final int progress;
  final VoidCallback onCreateResume;
  final VoidCallback? onPreview;
  final void Function(String, String) onOpenFeature;

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.fromLTRB(22, 25, 22, 32),
      children: [
        Text('Career Studio',
            style: Theme.of(context).textTheme.headlineMedium),
        const SizedBox(height: 5),
        Text(
          'Your professional story, shaped around the opportunity you want.',
          style: Theme.of(context).textTheme.bodyMedium,
        ),
        const SizedBox(height: 22),
        _SurfaceCard(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const _Eyebrow(
                  icon: Icons.description_outlined, label: 'RESUME STUDIO'),
              const SizedBox(height: 12),
              Text(
                progress == 0 ? 'Create your first resume' : 'Your resume draft',
                style: Theme.of(context).textTheme.titleLarge,
              ),
              const SizedBox(height: 7),
              Text(
                progress == 0
                    ? 'Start with the information you have. Your first draft does not need to be perfect.'
                    : 'Your saved draft is $progress% complete. Continue editing or preview it.',
                style: Theme.of(context).textTheme.bodyMedium,
              ),
              const SizedBox(height: 16),
              FilledButton.icon(
                onPressed: onCreateResume,
                icon: const Icon(Icons.edit_outlined),
                label: Text(
                    progress == 0 ? 'Start building' : 'Continue editing'),
              ),
              if (onPreview != null) ...[
                const SizedBox(height: 8),
                OutlinedButton.icon(
                  onPressed: onPreview,
                  icon: const Icon(Icons.visibility_outlined),
                  label: const Text('Preview resume'),
                ),
              ],
            ],
          ),
        ),
        const SizedBox(height: 15),
        _FeatureRowCard(
          icon: Icons.track_changes_outlined,
          title: 'ATS and job matching',
          description:
              'Compare your resume with a real job description and understand evidence gaps.',
          badge: 'PLANNED',
          onTap: () => onOpenFeature(
            'ATS and job matching',
            'This screen will compare a resume with a job description and explain skill alignment, missing evidence and document-readability checks.',
          ),
        ),
        const SizedBox(height: 11),
        _FeatureRowCard(
          icon: Icons.school_outlined,
          title: 'Academic CV and SOP',
          description:
              'Prepare an academic profile and statement of purpose for applications.',
          badge: 'PLANNED',
          onTap: () => onOpenFeature(
            'Academic CV and SOP',
            'This workflow will help students prepare a truthful academic CV and a program-specific statement of purpose.',
          ),
        ),
        const SizedBox(height: 11),
        _FeatureRowCard(
          icon: Icons.link_rounded,
          title: 'Career profile',
          description:
              'A reusable source of truth for all your tailored documents.',
          badge: 'PLANNED',
          onTap: () => onOpenFeature(
            'Career profile',
            'Your canonical profile will hold approved facts, skills, education, projects and work history so you can create targeted documents without re-entering everything.',
          ),
        ),
      ],
    );
  }
}

class _SoulCoachView extends StatelessWidget {
  const _SoulCoachView({required this.onOpenFeature});

  final void Function(String, String) onOpenFeature;

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.fromLTRB(22, 25, 22, 32),
      children: [
        Text('SoulCoach', style: Theme.of(context).textTheme.headlineMedium),
        const SizedBox(height: 5),
        Text(
          'Practical guidance for the next step in your career.',
          style: Theme.of(context).textTheme.bodyMedium,
        ),
        const SizedBox(height: 21),
        Container(
          padding: const EdgeInsets.all(21),
          decoration: BoxDecoration(
            gradient: const LinearGradient(
              colors: [Color(0xFF31245F), Color(0xFF6656D5)],
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
            ),
            borderRadius: BorderRadius.circular(22),
          ),
          child: const Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Icon(Icons.psychology_alt_rounded,
                  color: Color(0xFFE5DEFF), size: 31),
              SizedBox(height: 14),
              Text(
                'A thoughtful career companion.',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 23,
                  height: 1.16,
                  fontWeight: FontWeight.w800,
                ),
              ),
              SizedBox(height: 8),
              Text(
                'Prepare with clarity, learn from each step and stay in control of your career decisions.',
                style: TextStyle(
                  color: Color(0xFFE8E3FF),
                  fontSize: 12,
                  height: 1.5,
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 23),
        Text('Choose what you want to work on',
            style: Theme.of(context).textTheme.titleLarge),
        const SizedBox(height: 12),
        _FeatureRowCard(
          icon: Icons.record_voice_over_outlined,
          title: 'Practice an interview',
          description: 'Prepare structured answers for a target role.',
          badge: 'PLANNED',
          onTap: () => onOpenFeature(
            'Interview practice',
            'The interview coach will provide role-specific practice questions, answer frameworks and feedback. Live AI coaching is not connected in this preview.',
          ),
        ),
        const SizedBox(height: 10),
        _FeatureRowCard(
          icon: Icons.route_outlined,
          title: 'Plan my career move',
          description: 'Explore strengths, transferable skills and next steps.',
          badge: 'PLANNED',
          onTap: () => onOpenFeature(
            'Career planning',
            'Career planning will help you clarify your target role, identify transferable skills and build a practical development plan.',
          ),
        ),
        const SizedBox(height: 10),
        _FeatureRowCard(
          icon: Icons.auto_awesome_outlined,
          title: 'Improve my professional story',
          description: 'Turn your real experience into clear, specific evidence.',
          badge: 'AVAILABLE IN RESUME STUDIO',
          onTap: () => onOpenFeature(
            'Professional story',
            'You can currently improve your professional summary in Resume Studio when the Python AI service is configured.',
          ),
        ),
        const SizedBox(height: 16),
        const _SurfaceCard(
          color: Color(0xFFF5F3FF),
          child: Text(
            'SoulCoach is designed to support your decisions, not make career choices for you. Review recommendations and keep your own judgment at the center.',
            style: TextStyle(
              color: Color(0xFF615985),
              fontSize: 12,
              height: 1.5,
            ),
          ),
        ),
      ],
    );
  }
}

class _SoulMindView extends StatelessWidget {
  const _SoulMindView({
    required this.checkIn,
    required this.onClearCheckIn,
  });

  final String? checkIn;
  final VoidCallback onClearCheckIn;

  static const _affirmations = <String>[
    'My worth is not defined by a job title or an interview outcome.',
    'I can learn, adapt and communicate the value I bring.',
    'I allow myself to take the next step at a steady pace.',
  ];

  Future<void> _startPractice(BuildContext context) async {
    await showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      showDragHandle: true,
      backgroundColor: Colors.white,
      builder: (_) => const _ReflectionPracticeSheet(),
    );
  }

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.fromLTRB(22, 25, 22, 34),
      children: [
        Text('SoulMind', style: Theme.of(context).textTheme.headlineMedium),
        const SizedBox(height: 5),
        Text(
          'A little space for confidence, self-kindness and reflection.',
          style: Theme.of(context).textTheme.bodyMedium,
        ),
        if (checkIn != null) ...[
          const SizedBox(height: 15),
          _SurfaceCard(
            color: const Color(0xFFF3F0FF),
            child: Row(
              children: [
                const Icon(Icons.favorite_rounded,
                    color: SoulSkillTheme.violet),
                const SizedBox(width: 10),
                Expanded(
                  child: Text(
                    'You checked in: $checkIn. Let’s take this one step at a time.',
                    style: const TextStyle(
                      color: Color(0xFF625A8C),
                      fontSize: 12,
                      height: 1.4,
                    ),
                  ),
                ),
                IconButton(
                  tooltip: 'Clear check-in',
                  onPressed: onClearCheckIn,
                  icon: const Icon(Icons.close, size: 17),
                ),
              ],
            ),
          ),
        ],
        const SizedBox(height: 21),
        Container(
          padding: const EdgeInsets.all(23),
          decoration: BoxDecoration(
            gradient: const LinearGradient(
              colors: [Color(0xFFF0ECFF), Color(0xFFFFF2F8)],
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
            ),
            borderRadius: BorderRadius.circular(23),
          ),
          child: const Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _Eyebrow(
                icon: Icons.wb_twilight_rounded,
                label: 'TODAY’S AFFIRMATION',
                color: SoulSkillTheme.violet,
              ),
              SizedBox(height: 18),
              Text(
                'I am allowed to grow at my own pace. Every honest step I take is progress.',
                style: TextStyle(
                  color: SoulSkillTheme.ink,
                  fontSize: 22,
                  height: 1.25,
                  fontWeight: FontWeight.w800,
                  letterSpacing: -0.4,
                ),
              ),
              SizedBox(height: 13),
              Text(
                'Take a breath. Read it slowly, and keep the words that feel helpful to you.',
                style: TextStyle(
                  color: Color(0xFF716B91),
                  fontSize: 12,
                  height: 1.45,
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 24),
        Text('Affirmations for your journey',
            style: Theme.of(context).textTheme.titleLarge),
        const SizedBox(height: 11),
        ..._affirmations.map(
          (affirmation) => Padding(
            padding: const EdgeInsets.only(bottom: 9),
            child: _SurfaceCard(
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Icon(Icons.spa_outlined,
                      color: SoulSkillTheme.violet, size: 19),
                  const SizedBox(width: 11),
                  Expanded(
                    child: Text(
                      affirmation,
                      style: const TextStyle(
                        color: SoulSkillTheme.ink,
                        fontSize: 13,
                        height: 1.45,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
        const SizedBox(height: 16),
        _SurfaceCard(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const _Eyebrow(
                icon: Icons.self_improvement_rounded,
                label: 'HO’OPONOPONO-INSPIRED REFLECTION',
              ),
              const SizedBox(height: 10),
              Text(
                'A gentle pause to release self-judgment.',
                style: Theme.of(context).textTheme.titleLarge,
              ),
              const SizedBox(height: 7),
              Text(
                'Use the four familiar phrases as a personal reflection practice. There is no required belief or promised outcome.',
                style: Theme.of(context).textTheme.bodyMedium,
              ),
              const SizedBox(height: 15),
              SizedBox(
                width: double.infinity,
                child: FilledButton.icon(
                  onPressed: () => _startPractice(context),
                  icon: const Icon(Icons.play_arrow_rounded),
                  label: const Text('Begin a 2-minute reflection'),
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 15),
        const Text(
          'SoulMind offers optional wellbeing reflections, not mental-health diagnosis or treatment. You can skip any practice that does not feel right for you.',
          style: TextStyle(
            color: SoulSkillTheme.muted,
            fontSize: 10.5,
            height: 1.45,
          ),
        ),
      ],
    );
  }
}

class _ReflectionPracticeSheet extends StatefulWidget {
  const _ReflectionPracticeSheet();

  @override
  State<_ReflectionPracticeSheet> createState() =>
      _ReflectionPracticeSheetState();
}

class _ReflectionPracticeSheetState extends State<_ReflectionPracticeSheet> {
  int _step = 0;

  static const _steps = <(String, String)>[
    ('I’m sorry.', 'I acknowledge the pressure and disappointment I may be carrying.'),
    ('Please forgive me.', 'I choose to soften the harsh judgments I have placed on myself.'),
    ('Thank you.', 'I am grateful for what I have learned and the strengths I continue to build.'),
    ('I love you.', 'I choose to treat myself with patience, kindness and respect.'),
  ];

  @override
  Widget build(BuildContext context) {
    final current = _steps[_step];
    final isLast = _step == _steps.length - 1;

    return SafeArea(
      child: Padding(
        padding: EdgeInsets.fromLTRB(
          24,
          8,
          24,
          24 + MediaQuery.viewInsetsOf(context).bottom,
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const _Eyebrow(
              icon: Icons.self_improvement_rounded,
              label: 'A GENTLE REFLECTION',
            ),
            const SizedBox(height: 18),
            Text(
              'Step ${_step + 1} of ${_steps.length}',
              style: const TextStyle(
                color: SoulSkillTheme.muted,
                fontSize: 11,
                fontWeight: FontWeight.w700,
              ),
            ),
            const SizedBox(height: 7),
            ClipRRect(
              borderRadius: BorderRadius.circular(20),
              child: LinearProgressIndicator(
                value: (_step + 1) / _steps.length,
                minHeight: 6,
                backgroundColor: const Color(0xFFECEAFF),
                valueColor:
                    const AlwaysStoppedAnimation(SoulSkillTheme.violet),
              ),
            ),
            const SizedBox(height: 25),
            Text(
              current.$1,
              style: const TextStyle(
                color: SoulSkillTheme.ink,
                fontSize: 29,
                fontWeight: FontWeight.w800,
              ),
            ),
            const SizedBox(height: 10),
            Text(
              current.$2,
              style: const TextStyle(
                color: SoulSkillTheme.muted,
                fontSize: 14,
                height: 1.55,
              ),
            ),
            const SizedBox(height: 26),
            SizedBox(
              width: double.infinity,
              child: FilledButton(
                onPressed: () {
                  if (isLast) {
                    Navigator.of(context).pop();
                  } else {
                    setState(() => _step += 1);
                  }
                },
                child: Text(isLast ? 'Complete reflection' : 'Continue'),
              ),
            ),
            Center(
              child: TextButton(
                onPressed: () => Navigator.of(context).pop(),
                child: const Text('Close practice'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _FeaturePreviewScreen extends StatelessWidget {
  const _FeaturePreviewScreen({
    required this.title,
    required this.description,
  });

  final String title;
  final String description;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('SoulSkill')),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 520),
          child: Padding(
            padding: const EdgeInsets.all(22),
            child: _SurfaceCard(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Icon(Icons.auto_awesome_rounded,
                      color: SoulSkillTheme.violet, size: 30),
                  const SizedBox(height: 17),
                  Text(title,
                      style: Theme.of(context).textTheme.headlineMedium),
                  const SizedBox(height: 10),
                  Text(description,
                      style: Theme.of(context).textTheme.bodyLarge),
                  const SizedBox(height: 18),
                  const _Eyebrow(
                    icon: Icons.construction_outlined,
                    label: 'PRODUCT ROADMAP',
                  ),
                  const SizedBox(height: 16),
                  FilledButton(
                    onPressed: () => Navigator.of(context).pop(),
                    child: const Text('Back to SoulSkill'),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class _FeatureRowCard extends StatelessWidget {
  const _FeatureRowCard({
    required this.icon,
    required this.title,
    required this.description,
    required this.badge,
    required this.onTap,
  });

  final IconData icon;
  final String title;
  final String description;
  final String badge;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.white,
      borderRadius: BorderRadius.circular(17),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(17),
        child: Container(
          padding: const EdgeInsets.all(15),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(17),
            border: Border.all(color: SoulSkillTheme.border),
          ),
          child: Row(
            children: [
              Container(
                width: 42,
                height: 42,
                decoration: BoxDecoration(
                  color: const Color(0xFFECEAFF),
                  borderRadius: BorderRadius.circular(13),
                ),
                child: Icon(icon, color: SoulSkillTheme.violet, size: 21),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      title,
                      style: const TextStyle(
                        color: SoulSkillTheme.ink,
                        fontSize: 13,
                        fontWeight: FontWeight.w800,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      description,
                      style: const TextStyle(
                        color: SoulSkillTheme.muted,
                        fontSize: 11,
                        height: 1.4,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(width: 9),
              Column(
                children: [
                  Text(
                    badge,
                    style: const TextStyle(
                      color: Color(0xFF9299A7),
                      fontSize: 8,
                      fontWeight: FontWeight.w800,
                    ),
                  ),
                  const SizedBox(height: 4),
                  const Icon(Icons.chevron_right_rounded,
                      color: SoulSkillTheme.muted),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _SurfaceCard extends StatelessWidget {
  const _SurfaceCard({required this.child, this.color = Colors.white});

  final Widget child;
  final Color color;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: color,
        borderRadius: BorderRadius.circular(19),
        border: Border.all(color: SoulSkillTheme.border),
      ),
      child: child,
    );
  }
}

class _Eyebrow extends StatelessWidget {
  const _Eyebrow({
    required this.icon,
    required this.label,
    this.color = SoulSkillTheme.violet,
  });

  final IconData icon;
  final String label;
  final Color color;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Icon(icon, color: color, size: 17),
        const SizedBox(width: 7),
        Text(
          label,
          style: TextStyle(
            color: color,
            fontSize: 9,
            fontWeight: FontWeight.w800,
            letterSpacing: 1,
          ),
        ),
      ],
    );
  }
}
