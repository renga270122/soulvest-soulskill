import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:soulskill_mobile/main.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  setUp(() {
    SharedPreferences.setMockInitialValues({});
  });

  testWidgets('shows SoulSkill dashboard and opens Resume Studio', (tester) async {
    await tester.pumpWidget(const SoulSkillApp());
    await tester.pumpAndSettle();

    expect(find.text('SoulSkill'), findsOneWidget);
    expect(find.text('Make your next move\ncount.'), findsOneWidget);
    expect(find.text('Start building'), findsOneWidget);

    await tester.tap(find.text('Start building'));
    await tester.pumpAndSettle();

    expect(find.text('Resume Studio'), findsOneWidget);
    expect(find.text('Personal details'), findsOneWidget);
  });
}
