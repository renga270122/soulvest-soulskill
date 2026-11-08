enum CareerPath {
  freshGraduate,
  careerRestart,
  jobSwitcher,
  admissions,
}

extension CareerPathDetails on CareerPath {
  String get storageKey {
    switch (this) {
      case CareerPath.freshGraduate:
        return 'fresh_graduate';
      case CareerPath.careerRestart:
        return 'career_restart';
      case CareerPath.jobSwitcher:
        return 'job_switcher';
      case CareerPath.admissions:
        return 'admissions';
    }
  }

  String get label {
    switch (this) {
      case CareerPath.freshGraduate:
        return 'Fresh graduate';
      case CareerPath.careerRestart:
        return 'Career restart';
      case CareerPath.jobSwitcher:
        return 'Job switcher';
      case CareerPath.admissions:
        return 'Higher studies';
    }
  }

  String get description {
    switch (this) {
      case CareerPath.freshGraduate:
        return 'Build your first professional profile and prepare for entry-level roles.';
      case CareerPath.careerRestart:
        return 'Rebuild momentum, refresh your resume and plan your return to work.';
      case CareerPath.jobSwitcher:
        return 'Showcase your experience and prepare for your next opportunity.';
      case CareerPath.admissions:
        return 'Organize your academic story and prepare for university applications.';
    }
  }

  String get focusSummary {
    switch (this) {
      case CareerPath.freshGraduate:
        return 'Turn your education, projects and strengths into your first career story.';
      case CareerPath.careerRestart:
        return 'Take your next step at your own pace. Your experience still has value.';
      case CareerPath.jobSwitcher:
        return 'Connect your experience to the roles and opportunities you want next.';
      case CareerPath.admissions:
        return 'Build a clear academic profile for the programs you want to pursue.';
    }
  }

  String get targetLabel =>
      this == CareerPath.admissions ? 'Target program or field' : 'Target role';

  String get targetHint => this == CareerPath.admissions
      ? 'e.g. MSc Data Science, MBA, PhD in Biology'
      : 'e.g. Product Designer, Data Analyst, Software Engineer';

  static CareerPath fromStorage(String? value) {
    return CareerPath.values.firstWhere(
      (path) => path.storageKey == value,
      orElse: () => CareerPath.jobSwitcher,
    );
  }
}

class UserProfileModel {
  const UserProfileModel({
    this.fullName = '',
    this.email = '',
    this.city = '',
    this.country = '',
    this.targetRole = '',
    this.experienceLevel = 'Not sure yet',
    this.careerPath = CareerPath.jobSwitcher,
    this.updatedAt = '',
  });

  final String fullName;
  final String email;
  final String city;
  final String country;
  final String targetRole;
  final String experienceLevel;
  final CareerPath careerPath;
  final String updatedAt;

  String get firstName {
    final trimmed = fullName.trim();
    if (trimmed.isEmpty) return '';
    return trimmed.split(RegExp(r'\s+')).first;
  }

  String get locationLabel {
    return [city.trim(), country.trim()]
        .where((value) => value.isNotEmpty)
        .join(', ');
  }

  int get completionPercent {
    final fields = <bool>[
      fullName.trim().isNotEmpty,
      email.trim().isNotEmpty,
      city.trim().isNotEmpty,
      country.trim().isNotEmpty,
      targetRole.trim().isNotEmpty,
      experienceLevel != 'Not sure yet',
    ];
    return ((fields.where((complete) => complete).length / fields.length) * 100)
        .round();
  }

  UserProfileModel copyWith({
    String? fullName,
    String? email,
    String? city,
    String? country,
    String? targetRole,
    String? experienceLevel,
    CareerPath? careerPath,
    String? updatedAt,
  }) {
    return UserProfileModel(
      fullName: fullName ?? this.fullName,
      email: email ?? this.email,
      city: city ?? this.city,
      country: country ?? this.country,
      targetRole: targetRole ?? this.targetRole,
      experienceLevel: experienceLevel ?? this.experienceLevel,
      careerPath: careerPath ?? this.careerPath,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }

  Map<String, dynamic> toJson() => {
        'fullName': fullName,
        'email': email,
        'city': city,
        'country': country,
        'targetRole': targetRole,
        'experienceLevel': experienceLevel,
        'careerPath': careerPath.storageKey,
        'updatedAt': updatedAt,
      };

  factory UserProfileModel.fromJson(Map<String, dynamic> json) {
    return UserProfileModel(
      fullName: json['fullName'] as String? ?? '',
      email: json['email'] as String? ?? '',
      city: json['city'] as String? ?? '',
      country: json['country'] as String? ?? '',
      targetRole: json['targetRole'] as String? ?? '',
      experienceLevel: json['experienceLevel'] as String? ?? 'Not sure yet',
      careerPath: CareerPathDetails.fromStorage(json['careerPath'] as String?),
      updatedAt: json['updatedAt'] as String? ?? '',
    );
  }
}
