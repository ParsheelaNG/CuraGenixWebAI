CREATE DATABASE chronicdisease;
USE chronicdisease;
CREATE TABLE chronic(
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255),
    Age INT NOT NULL,
    Sex INT NOT NULL,
    HighChol INT NOT NULL,
    CholCheck INT NOT NULL,
    BMI INT NOT NULL,
    Smoker INT NOT NULL,
    HeartDiseaseorAttack INT NOT NULL,
    PhysActivity INT NOT NULL,
    Fruits INT NOT NULL,
    Veggies INT NOT NULL,
    HvyAlcoholConsump INT NOT NULL,
    GenHlth INT NOT NULL,
    MentHlth INT NOT NULL,
    PhysHlth INT NOT NULL,
    DiffWalk INT NOT NULL
);
truncate chronic;
drop table chronic;
SELECT * FROM chronic;
select * from signup;
create table signup(Id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, Username varchar(100),Password varchar(300),MailID varchar(100),PhoneNumber varchar(100),Place varchar(100));
truncate table signup;
