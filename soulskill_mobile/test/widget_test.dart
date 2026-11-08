import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:provider/provider.dart';
import 'package:soulskill_mobile/providers/resume_provider.dart';
import 'package:soulskill_mobile/main.dart';
import 'package:soulskill_mobile/screens/job_targeting_screen.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  setUp(() {
    SharedPreferences.setMockInitialValues({});
  });

  testWidgets('shows responsive SoulSkill dashboard and opens Resume Studio',
      (tester) async {
    await tester.pumpWidget(const SoulSkillApp());
    await tester.pumpAndSettle();

    expect(find.text('SoulSkill'), findsOneWidget);
    expect(find.text('Welcome to your next chapter'), findsOneWidget);
    expect(find.text('Create / improve resume'), findsOneWidget);
    await tester.tap(find.text('Create / improve resume'));
    await tester.pumpAndSettle();

    expect(find.text('Resume Studio'), findsOneWidget);
    expect(find.text('Personal details'), findsOneWidget);
  });

  testWidgets('opens SoulMind and completes the guided reflection',
      (tester) async {
    await tester.pumpWidget(const SoulSkillApp());
    await tester.pumpAndSettle();

    await tester.tap(find.text('SoulMind').last);
    await tester.pumpAndSettle();

    expect(find.text('TODAY’S AFFIRMATION'), findsOneWidget);
    await tester.drag(find.byType(ListView).last, const Offset(0, -600));
    await tester.pumpAndSettle();
    await tester.ensureVisible(find.text('Begin a 2-minute reflection'));
    await tester.pumpAndSettle();
    expect(find.text('Begin a 2-minute reflection'), findsOneWidget);

    await tester.tap(find.text('Begin a 2-minute reflection'));
    await tester.pumpAndSettle();

    expect(find.text('I’m sorry.'), findsOneWidget);
    await tester.tap(find.text('Continue'));
    await tester.pumpAndSettle();
    expect(find.text('Please forgive me.'), findsOneWidget);
    await tester.tap(find.text('Continue'));
    await tester.pumpAndSettle();
    expect(find.text('Thank you.'), findsOneWidget);
    await tester.tap(find.text('Continue'));
    await tester.pumpAndSettle();
    expect(find.text('I love you.'), findsOneWidget);

    await tester.tap(find.text('Complete reflection'));
    await tester.pumpAndSettle();
    expect(find.text('Begin a 2-minute reflection'), findsOneWidget);
  });

  testWidgets('uses desktop navigation at wide viewport', (tester) async {
    tester.view.physicalSize = const Size(1440, 1000);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);

    await tester.pumpWidget(const SoulSkillApp());
    await tester.pumpAndSettle();

    expect(find.text('WORKSPACE'), findsOneWidget);
    expect(find.text('Career Studio'), findsOneWidget);
    expect(find.text('A global career workspace'), findsOneWidget);

    await tester.tap(find.text('SoulMind').first);
    await tester.pumpAndSettle();
    expect(find.text('Affirmations for your journey'), findsOneWidget);
  });

  testWidgets('shows the resume-to-interview job targeting workflow',
      (tester) async {
    await tester.pumpWidget(
      ChangeNotifierProvider(
        create: (_) => ResumeProvider()..load(),
        child: const MaterialApp(home: JobTargetingScreen()),
      ),
    );
    await tester.pumpAndSettle();

    expect(find.text('Resume to Interview'), findsOneWidget);
    expect(find.text('Import PDF, DOCX or TXT resume'), findsOneWidget);
    expect(find.text('Target role'), findsOneWidget);
    expect(find.text('Job description'), findsOneWidget);
    expect(find.text('Analyze my job fit'), findsOneWidget);
  });

}
