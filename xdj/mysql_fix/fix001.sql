SET @db_type ="date";
SET @dbname = DATABASE();
SET @tablename = "course_overviews_courseoverview";
SET @columnname = "certificate_available_date";
SET @preparedStatement = (SELECT IF(
  (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE
      (table_name = @tablename)
      AND (table_schema = @dbname)
      AND (column_name = @columnname)
  ) > 0,
  "SELECT 1",
  CONCAT("ALTER TABLE ", @tablename, " ADD ", @columnname, " ",@db_type,";")
));

PREPARE alterIfNotExists FROM @preparedStatement;
EXECUTE alterIfNotExists;
DEALLOCATE PREPARE alterIfNotExists;


SET @db_type ="int(11)";
SET @dbname = DATABASE();
SET @tablename = "student_courseenrollmentallowed";
SET @columnname = "user_id";
SET @preparedStatement = (SELECT IF(
  (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE
      (table_name = @tablename)
      AND (table_schema = @dbname)
      AND (column_name = @columnname)
  ) > 0,
  "SELECT 1",
  CONCAT("ALTER TABLE ", @tablename, " ADD ", @columnname, " ",@db_type,";")
));


PREPARE alterIfNotExists FROM @preparedStatement;
EXECUTE alterIfNotExists;
DEALLOCATE PREPARE alterIfNotExists;

SET @db_type ="date";
SET @dbname = DATABASE();
SET @tablename = "social_auth_partial";
SET @columnname = "timestamp";
SET @preparedStatement = (SELECT IF(
  (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE
      (table_name = @tablename)
      AND (table_schema = @dbname)
      AND (column_name = @columnname)
  ) > 0,
  "SELECT 1",
  CONCAT("ALTER TABLE ", @tablename, " ADD ", @columnname, " ",@db_type,";")
));
PREPARE stmt1 FROM @preparedStatement;
EXECUTE stmt1;
DEALLOCATE PREPARE stmt1;


CREATE TABLE entitlements_courseentitlement (
  id int(11) NOT NULL AUTO_INCREMENT,
  created datetime(6) NOT NULL,
  modified datetime(6) NOT NULL,
  uuid char(32) NOT NULL,
  course_uuid char(32) NOT NULL,
  expired_at datetime(6) DEFAULT NULL,
  mode varchar(100) NOT NULL,
  order_number varchar(128) DEFAULT NULL,
  enrollment_course_run_id' int(11) DEFAULT NULL,
  user_id int(11) NOT NULL,
  _policy_id int(11) DEFAULT NULL,
  refund_locked tinyint(1) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY entitlements_courseentitlement_uuid_a690dd005d0695b_uniq (uuid),
  KEY entitlements_courseentit_user_id_a8df050144d72f8_fk_auth_user_id (user_id),
  KEY fda6bce9129c5afc395658f36b9d444e (enrollment_course_run_id),
  KEY entitlements_courseentitlement_36cddc86 (_policy_id),
  CONSTRAINT D2cebc0610e28b9b3a821c839e2fe01c FOREIGN KEY (_policy_id) REFERENCES entitlements_courseentitlementpolicy (id),
  CONSTRAINT entitlements_courseentitlement_user_id_a518a225_fk FOREIGN KEY (user_id) REFERENCES auth_user (id),
  CONSTRAINT fda6bce9129c5afc395658f36b9d444e FOREIGN KEY (enrollment_course_run_id) REFERENCES student_courseenrollment (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE video_pipeline_videouploadsenabledbydefault (
  id int(11) NOT NULL AUTO_INCREMENT,
  change_date datetime(6) NOT NULL,
  enabled tinyint(1) NOT NULL,
  enabled_for_all_courses tinyint(1) NOT NULL,
  changed_by_id int(11) DEFAULT NULL,
  PRIMARY KEY (id),
  KEY video_pipeline_vi_changed_by_id_4fff17e91cce415c_fk_auth_user_id (changed_by_id),
  CONSTRAINT video_pipeline_videouploa_changed_by_id_3d066822_fk FOREIGN KEY (changed_by_id) REFERENCES auth_user (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE verify_student_ssoverification (
  id int(11) NOT NULL AUTO_INCREMENT,
  status varchar(100) NOT NULL,
  status_changed datetime(6) NOT NULL,
  name varchar(255) NOT NULL,
  created_at datetime(6) NOT NULL,
  updated_at datetime(6) NOT NULL,
  identity_provider_type varchar(100) NOT NULL,
  identity_provider_slug varchar(30) NOT NULL,
  user_id int(11) NOT NULL,
  PRIMARY KEY (id),
  KEY verify_student_ssoverification_user_id_5e6186eb_fk_auth_user_id (user_id),
  KEY verify_student_ssoverification_created_at_6381e5a4 (created_at),
  KEY verify_student_ssoverification_updated_at_9d6cc952 (updated_at),
  KEY verify_student_ssoverification_identity_provider_slug_56c53eb6 (identity_provider_slug),
  CONSTRAINT verify_student_ssoverification_user_id_5e6186eb_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE verify_student_manualverification (
  id int(11) NOT NULL AUTO_INCREMENT,
  status varchar(100) NOT NULL,
  status_changed datetime(6) NOT NULL,
  name varchar(255) NOT NULL,
  created_at datetime(6) NOT NULL,
  updated_at datetime(6) NOT NULL,
  reason varchar(255) NOT NULL,
  user_id int(11) NOT NULL,
  PRIMARY KEY (id),
  KEY verify_student_manua_user_id_f38b72b4_fk_auth_user (user_id),
  KEY verify_student_manualverification_created_at_e4e3731a (created_at),
  KEY verify_student_manualverification_updated_at_1a350690 (updated_at),
  CONSTRAINT verify_student_manua_user_id_f38b72b4_fk_auth_user FOREIGN KEY (user_id) REFERENCES auth_user (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE coursewarehistoryextended_studentmodulehistoryextended (
  version varchar(255) DEFAULT NULL,
  created datetime(6) NOT NULL,
  state longtext,
  grade double DEFAULT NULL,
  max_grade double DEFAULT NULL,
  id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  student_module_id int(11) NOT NULL,
  PRIMARY KEY (id),
  KEY coursewarehistoryextended_studentmodulehistoryextended_2af72f10 (version),
  KEY coursewarehistoryextended_studentmodulehistoryextended_e2fa5388 (created),
  KEY coursewarehistoryextended_student_module_id_61b23a7a1dd27fe4_idx (student_module_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE email_marketing_emailmarketingconfiguration;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE email_marketing_emailmarketingconfiguration (
  id int(11) NOT NULL AUTO_INCREMENT,
  change_date datetime(6) NOT NULL,
  enabled tinyint(1) NOT NULL,
  sailthru_key varchar(32) NOT NULL,
  sailthru_secret varchar(32) NOT NULL,
  sailthru_new_user_list varchar(48) NOT NULL,
  sailthru_retry_interval int(11) NOT NULL,
  sailthru_max_retries int(11) NOT NULL,
  changed_by_id int(11) DEFAULT NULL,
  sailthru_abandoned_cart_delay int(11) NOT NULL,
  sailthru_abandoned_cart_template varchar(20) NOT NULL,
  sailthru_content_cache_age int(11) NOT NULL,
  sailthru_enroll_cost int(11) NOT NULL,
  sailthru_enroll_template varchar(20) NOT NULL,
  sailthru_get_tags_from_sailthru tinyint(1) NOT NULL,
  sailthru_purchase_template varchar(20) NOT NULL,
  sailthru_upgrade_template varchar(20) NOT NULL,
  sailthru_lms_url_override varchar(80) NOT NULL,
  welcome_email_send_delay int(11) NOT NULL,
  user_registration_cookie_timeout_delay double NOT NULL,
  sailthru_welcome_template varchar(20) NOT NULL,
  sailthru_verification_failed_template varchar(20) NOT NULL,
  sailthru_verification_passed_template varchar(20) NOT NULL,
  PRIMARY KEY (id),
  KEY email_marketing_e_changed_by_id_1c6968b921f23b0b_fk_auth_user_id (changed_by_id),
  CONSTRAINT email_marketing_emailmark_changed_by_id_15ce753b_fk FOREIGN KEY (changed_by_id) REFERENCES auth_user (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE student_sociallink (
  id int(11) NOT NULL AUTO_INCREMENT,
  platform varchar(30) NOT NULL,
  social_link varchar(100) NOT NULL,
  user_profile_id int(11) NOT NULL,
  PRIMARY KEY (id),
  KEY student_s_user_profile_id_7c5a1bfd4e58b3a_fk_auth_userprofile_id (user_profile_id),
  CONSTRAINT student_s_user_profile_id_7c5a1bfd4e58b3a_fk_auth_userprofile_id FOREIGN KEY (user_profile_id) REFERENCES auth_userprofile (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE courseware_dynamicupgradedeadlineconfiguration (
  id int(11) NOT NULL AUTO_INCREMENT,
  change_date datetime(6) NOT NULL,
  enabled tinyint(1) NOT NULL,
  deadline_days smallint(5) unsigned NOT NULL,
  changed_by_id int(11) DEFAULT NULL,
  PRIMARY KEY (id),
  KEY courseware_dynami_changed_by_id_77da0c73df07c112_fk_auth_user_id (changed_by_id),
  CONSTRAINT courseware_dynamicupgrade_changed_by_id_6a450e2c_fk FOREIGN KEY (changed_by_id) REFERENCES auth_user (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



