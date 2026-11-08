class ResumeModel {
  const ResumeModel({
    this.fullName = '',
    this.targetRole = '',
    this.email = '',
    this.phone = '',
    this.location = '',
    this.professionalSummary = '',
    this.experienceRole = '',
    this.company = '',
    this.experienceDescription = '',
    this.degree = '',
    this.institution = '',
    this.educationDetails = '',
    this.skills = '',
    this.updatedAt = '',
  });

  final String fullName;
  final String targetRole;
  final String email;
  final String phone;
  final String location;
  final String professionalSummary;
  final String experienceRole;
  final String company;
  final String experienceDescription;
  final String degree;
  final String institution;
  final String educationDetails;
  final String skills;
  final String updatedAt;

  List<String> get skillList => skills
      .split(',')
      .map((skill) => skill.trim())
      .where((skill) => skill.isNotEmpty)
      .toSet()
      .toList();

  int get completionPercent {
    final checks = <bool>[
      fullName.trim().isNotEmpty,
      targetRole.trim().isNotEmpty,
      email.trim().isNotEmpty,
      phone.trim().isNotEmpty,
      professionalSummary.trim().isNotEmpty,
      experienceRole.trim().isNotEmpty || experienceDescription.trim().isNotEmpty,
      degree.trim().isNotEmpty || institution.trim().isNotEmpty,
      skillList.isNotEmpty,
    ];
    return ((checks.where((complete) => complete).length / checks.length) * 100)
        .round();
  }

  ResumeModel copyWith({
    String? fullName,
    String? targetRole,
    String? email,
    String? phone,
    String? location,
    String? professionalSummary,
    String? experienceRole,
    String? company,
    String? experienceDescription,
    String? degree,
    String? institution,
    String? educationDetails,
    String? skills,
    String? updatedAt,
  }) {
    return ResumeModel(
      fullName: fullName ?? this.fullName,
      targetRole: targetRole ?? this.targetRole,
      email: email ?? this.email,
      phone: phone ?? this.phone,
      location: location ?? this.location,
      professionalSummary: professionalSummary ?? this.professionalSummary,
      experienceRole: experienceRole ?? this.experienceRole,
      company: company ?? this.company,
      experienceDescription: experienceDescription ?? this.experienceDescription,
      degree: degree ?? this.degree,
      institution: institution ?? this.institution,
      educationDetails: educationDetails ?? this.educationDetails,
      skills: skills ?? this.skills,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }

  Map<String, dynamic> toJson() => {
        'fullName': fullName,
        'targetRole': targetRole,
        'email': email,
        'phone': phone,
        'location': location,
        'professionalSummary': professionalSummary,
        'experienceRole': experienceRole,
        'company': company,
        'experienceDescription': experienceDescription,
        'degree': degree,
        'institution': institution,
        'educationDetails': educationDetails,
        'skills': skills,
        'updatedAt': updatedAt,
      };

  factory ResumeModel.fromJson(Map<String, dynamic> json) {
    return ResumeModel(
      fullName: json['fullName'] as String? ?? '',
      targetRole: json['targetRole'] as String? ?? '',
      email: json['email'] as String? ?? '',
      phone: json['phone'] as String? ?? '',
      location: json['location'] as String? ?? '',
      professionalSummary: json['professionalSummary'] as String? ?? '',
      experienceRole: json['experienceRole'] as String? ?? '',
      company: json['company'] as String? ?? '',
      experienceDescription: json['experienceDescription'] as String? ?? '',
      degree: json['degree'] as String? ?? '',
      institution: json['institution'] as String? ?? '',
      educationDetails: json['educationDetails'] as String? ?? '',
      skills: json['skills'] as String? ?? '',
      updatedAt: json['updatedAt'] as String? ?? '',
    );
  }

  Map<String, dynamic> toApiJson() => {
        'name': fullName,
        'email': email,
        'phone': phone,
        'location': location,
        'professional_summary': professionalSummary,
        'work_experience': [
          if (experienceRole.isNotEmpty || company.isNotEmpty || experienceDescription.isNotEmpty)
            {
              'title': experienceRole,
              'company': company,
              'description': experienceDescription,
            }
        ],
        'education': [
          if (degree.isNotEmpty || institution.isNotEmpty || educationDetails.isNotEmpty)
            {
              'degree': degree,
              'institution': institution,
              'description': educationDetails,
            }
        ],
        'skills': skillList,
        'projects': <Map<String, String>>[],
        'certifications': <String>[],
        'industry': targetRole,
        'template_style': 'modern',
      };
}
