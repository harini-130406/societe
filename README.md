To install jdk 21
sudo apt update
sudo apt install openjdk-21-jdk -y

To select Java 21 as the default Java version, execute:
sudo update-alternatives --config java
sudo update-alternatives --config javac

export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export PATH="$JAVA_HOME/bin:$PATH"

java -version
javac -version
echo "$JAVA_HOME"

sudo apt update
sudo apt install maven -y

mvn -version


Then create a Maven project with a name and paste this code
package org.example;

import java.util.Scanner;
public class Main {
    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.print("Enter marks in Subject 1: ");
        double mark1 = sc.nextDouble();

        System.out.print("Enter marks in Subject 2: ");
        double mark2 = sc.nextDouble();

        System.out.print("Enter marks in Subject 3: ");
        double mark3 = sc.nextDouble();

        double average = (mark1 + mark2 + mark3) / 3;

        System.out.println("Average Marks: " + average);

        if (average >= 90) {
            System.out.println("Grade: A");
        } else if (average >= 75) {
            System.out.println("Grade: B");
        } else if (average >= 50) {
            System.out.println("Grade: C");
        } else {
            System.out.println("Grade: F");
        }

        sc.close();
    }
}

Pom.xml

<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         https://maven.apache.org/xsd/maven-4.0.0.xsd">

    <modelVersion>4.0.0</modelVersion>

    <groupId>org.example</groupId>
    <artifactId>Grade_Calculator</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.release>21</maven.compiler.release>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <build>
        <plugins>

            <!-- Java Compiler Plugin -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.13.0</version>
            </plugin>

            <!-- JAR Plugin -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-jar-plugin</artifactId>
                <version>3.4.2</version>
                <configuration>
                    <archive>
                        <manifest>
                            <mainClass>org.example.Main</mainClass>
                        </manifest>
                    </archive>
                </configuration>
            </plugin>

        </plugins>
    </build>

</project>

Then run
mvn clean package

Create git link with same name

git --version
git config --global user.name "harini-130406"
git config --global user.email "24z260@psgitech.ac.in"

git init
git add .
git commit -m "First commit - Grade Calculator"
git branch -M main
git remote add origin https://github.com/harini-130406/Grade_Calculator.git
git remote -v
git push -u origin main


# Maven build for Grade Calculator

trigger:
- main

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: Maven@3
  inputs:
    mavenPomFile: 'pom.xml'
    mavenOptions: '-Xmx3072m'
    javaHomeOption: 'JDKVersion'
    jdkVersionOption: '1.21'
    jdkArchitectureOption: 'x64'
    publishJUnitResults: true
    testResultsFiles: '**/surefire-reports/TEST-*.xml'
    goals: 'clean package'

- task: PublishBuildArtifacts@1
  inputs:
    PathtoPublish: '$(System.DefaultWorkingDirectory)/target'
    ArtifactName: 'GradeCalculator-JAR'
    publishLocation: 'Container'


package org.example;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.print("Enter electricity units consumed: ");
        double units = sc.nextDouble();

        double bill;

        if (units < 0) {
            System.out.println("Invalid units!");
            sc.close();
            return;
        }

        if (units <= 100) {
            bill = units * 1.50;
        } else if (units <= 200) {
            bill = (100 * 1.50)
                    + ((units - 100) * 2.50);
        } else {
            bill = (100 * 1.50)
                    + (100 * 2.50)
                    + ((units - 200) * 4.00);
        }

        System.out.println("Electricity Bill: Rs. " + bill);

        sc.close();
    }
}

Create a java class in org


package org.example;

public class Calculator {

    public int add(int a, int b) {
        return a + b;
    }

    public int subtract(int a, int b) {
        return a - b;
    }

    public int multiply(int a, int b) {
        return a * b;
    }

    public double divide(int a, int b) {
        if (b == 0) {
            throw new ArithmeticException("Cannot divide by zero");
        }
        return (double) a / b;
    }
}


Expand main → java → org.example.
Right-click org.example.
Select New → Java Class.
Enter Calculator.


package org.example;

public class Calculator {

    public int add(int a, int b) {
        return a + b;
    }

    public int subtract(int a, int b) {
        return a - b;
    }

    public int multiply(int a, int b) {
        return a * b;
    }

    public double divide(int a, int b) {
        if (b == 0) {
            throw new ArithmeticException("Cannot divide by zero");
        }
        return (double) a / b;
    }
}

Open the existing Main.java file under src/main/java/org.example.
Main.java

package org.example;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);
        Calculator calc = new Calculator();

        System.out.print("Enter first number: ");
        int a = sc.nextInt();

        System.out.print("Enter second number: ");
        int b = sc.nextInt();

        System.out.println("Addition: " + calc.add(a, b));
        System.out.println("Subtraction: " + calc.subtract(a, b));
        System.out.println("Multiplication: " + calc.multiply(a, b));

        try {
            System.out.println("Division: " + calc.divide(a, b));
        } catch (ArithmeticException e) {
            System.out.println(e.getMessage());
        }

        sc.close();
    }
}

pom.xml

<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         https://maven.apache.org/xsd/maven-4.0.0.xsd">

    <modelVersion>4.0.0</modelVersion>

    <groupId>org.example</groupId>
    <artifactId>Calculator_1</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.release>21</maven.compiler.release>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.13.1</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.13.0</version>
            </plugin>

            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.2.5</version>
            </plugin>

            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-jar-plugin</artifactId>
                <version>3.4.2</version>
                <configuration>
                    <archive>
                        <manifest>
                            <mainClass>org.example.Main</mainClass>
                        </manifest>
                    </archive>
                </configuration>
            </plugin>
        </plugins>
    </build>

</project>

mvn clean test
mvn clean package


trigger:
- main

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: Maven@3
  inputs:
    mavenPomFile: 'pom.xml'
    mavenOptions: '-Xmx3072m'
    javaHomeOption: 'JDKVersion'
    jdkVersionOption: '1.21'
    jdkArchitectureOption: 'x64'
    publishJUnitResults: true
    testResultsFiles: '**/surefire-reports/TEST-*.xml'
    goals: 'clean package'

- task: PublishBuildArtifacts@1
  inputs:
    PathtoPublish: '$(System.DefaultWorkingDirectory)/target'
    ArtifactName: 'Calculator-JAR'
    publishLocation: 'Container'


Student Result
Student.java
package org.example;

public class Student {
    public String checkResult(int marks) {
        if (marks < 0 || marks > 100) {
            throw new IllegalArgumentException("Invalid marks");
        }

        if (marks >= 50) {
            return "Pass";
        } else {
            return "Fail";
        }
    }
}
Main.java
package org.example;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Student student = new Student();

        System.out.print("Enter student marks: ");
        int marks = sc.nextInt();

        System.out.println("Result: " + student.checkResult(marks));

        sc.close();
    }
}
StudentTest.java
package org.example;

import org.junit.Test;
import static org.junit.Assert.*;

public class StudentTest {

    Student student = new Student();

    @Test
    public void testFail() {
        assertEquals("Fail", student.checkResult(35));
    }

    @Test
    public void testPassAt50() {
        assertEquals("Pass", student.checkResult(50));
    }

    @Test
    public void testPassAt75() {
        assertEquals("Pass", student.checkResult(75));
    }

    @Test
    public void testPassAt100() {
        assertEquals("Pass", student.checkResult(100));
    }
}

pom.xml

<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>org.example</groupId>
    <artifactId>Student_Result</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.release>21</maven.compiler.release>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.13.1</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.13.0</version>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.2.5</version>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-jar-plugin</artifactId>
                <version>3.4.2</version>
                <configuration>
                    <archive>
                        <manifest>
                            <mainClass>org.example.Main</mainClass>
                        </manifest>
                    </archive>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>


LeapYear.java
package org.example;

public class LeapYear {

    public boolean isLeapYear(int year) {
        if (year <= 0) {
            throw new IllegalArgumentException("Invalid year");
        }

        return (year % 400 == 0) ||
               (year % 4 == 0 && year % 100 != 0);
    }
}

Main.java
package org.example;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        LeapYear leap = new LeapYear();

        System.out.print("Enter year: ");
        int year = sc.nextInt();

        if (leap.isLeapYear(year)) {
            System.out.println(year + " is a Leap Year");
        } else {
            System.out.println(year + " is not a Leap Year");
        }

        sc.close();
    }
}

LeapYearTest.java
package org.example;

import org.junit.Test;
import static org.junit.Assert.*;

public class LeapYearTest {

    LeapYear leap = new LeapYear();

    @Test
    public void testLeapYear() {
        assertTrue(leap.isLeapYear(2024));
    }

    @Test
    public void testNonLeapYear() {
        assertFalse(leap.isLeapYear(2023));
    }

    @Test
    public void testCenturyNotLeapYear() {
        assertFalse(leap.isLeapYear(1900));
    }

    @Test
    public void testCenturyLeapYear() {
        assertTrue(leap.isLeapYear(2000));
    }
}

pom.xml

<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         https://maven.apache.org/xsd/maven-4.0.0.xsd">

    <modelVersion>4.0.0</modelVersion>
    <groupId>org.example</groupId>
    <artifactId>Leap_Year</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.release>21</maven.compiler.release>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.13.1</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.13.0</version>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.2.5</version>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-jar-plugin</artifactId>
                <version>3.4.2</version>
                <configuration>
                    <archive>
                        <manifest>
                            <mainClass>org.example.Main</mainClass>
                        </manifest>
                    </archive>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>


DiscountCalculator
package org.example;

public class DiscountCalculator {

    public double calculateFinalAmount(double amount) {
        if (amount < 0) {
            throw new IllegalArgumentException("Invalid amount");
        }

        if (amount >= 1000) {
            return amount - (amount * 0.10);
        } else {
            return amount;
        }
    }
}

Main.java
package org.example;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        DiscountCalculator calculator = new DiscountCalculator();

        System.out.print("Enter purchase amount: ");
        double amount = sc.nextDouble();

        double finalAmount = calculator.calculateFinalAmount(amount);

        System.out.println("Final amount: Rs. " + finalAmount);

        sc.close();
    }
}

DiscountCalculatorTest
package org.example;

import org.junit.Test;
import static org.junit.Assert.*;

public class DiscountCalculatorTest {

    DiscountCalculator calculator = new DiscountCalculator();

    @Test
    public void testBelow1000() {
        assertEquals(900.0, calculator.calculateFinalAmount(900), 0.001);
    }

    @Test
    public void testEqualTo1000() {
        assertEquals(900.0, calculator.calculateFinalAmount(1000), 0.001);
    }

    @Test
    public void testAbove1000() {
        assertEquals(1350.0, calculator.calculateFinalAmount(1500), 0.001);
    }
}


Jenkinss
sudo apt update
sudo apt install fontconfig openjdk-21-jre -y
sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc \
https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key

echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null

sudo apt update
sudo apt install jenkins -y


if error comes do this 
sudo mkdir -p /etc/apt/keyrings
sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
sudo chmod 644 /etc/apt/keyrings/jenkins-keyring.asc
sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key
sudo apt update
sudo apt install jenkins -y

sudo systemctl start jenkins
sudo systemctl status jenkins

http://localhost:8080

Then give
sudo cat /var/lib/jenkins/secrets/initialAdminPassword


pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/harini-130406/Gross_Salary.git'
            }
        }

        stage('Compile') {
            steps {
                sh 'mvn clean compile'
            }
        }

        stage('Execute') {
            steps {
                sh 'printf "50000\n10000\n5000\n" | java -cp target/classes org.example.Main'
            }
        }
    }
}


pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'YOUR_GITHUB_REPOSITORY_URL'
            }
        }

        stage('Compile') {
            steps {
                sh 'mvn clean compile'
            }
        }

        stage('Execute') {
            steps {
                sh 'YOUR_EXECUTION_COMMAND'
            }
        }
    }
}
Paindrome check
'printf "121\n" | java -cp target/classes org.example.Main'


10. printf "10\n" \| java -cp target/classes org.example.Main
11.printf "121\n" \| java -cp target/classes org.example.Main
12.printf "7\n" \| java -cp target/classes org.example.Main
fact
printf "5\n" \| java -cp target/classes org.example.Main
fibo
printf "7\n" \| java -cp target/classes org.example.Main



pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/harini-130406/Multiplication_Table.git'
            }
        }

        stage('Compile') {
            steps {
                sh 'mvn clean compile'
            }
        }

        stage('Execute') {
            steps {
                sh 'printf "10\n" | java -cp target/classes org.example.Main'
            }
        }
    }
}




Gradle project

gradle --version
java -version

sudo snap install gradle --classic
gradle init


gradle --version
java -version

sudo snap install gradle --classic
gradle init

cd "/mnt/c/Users/Subhaharini S K/Documents"
mkdir -p Gradle_Experiments
cd Gradle_Experiments
mkdir SimpleInterest
cd SimpleInterest
gradle init

nano app/src/main/java/org/example/App.java


package org.example;

import java.util.Scanner;

public class App {
    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.print("Enter length: ");
        double length = sc.nextDouble();

        System.out.print("Enter breadth: ");
        double breadth = sc.nextDouble();

        double area = length * breadth;

        double perimeter = 2 * (length + breadth);

        System.out.println("Area = " + area);
        System.out.println("Perimeter = " + perimeter);

        sc.close();
    }
}


nano app/build.gradle
plugins {
    id 'application'
}

repositories {
    mavenCentral()
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

application {
    mainClass = 'org.example.App'
}

tasks.named('run') {
    standardInput = System.in
}

rm app/src/test/java/org/example/AppTest.java
./gradlew clean build
./gradlew run


package org.example;

import java.util.Scanner;

public class App {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int[] numbers = new int[5];
        int sum = 0;

        System.out.println("Enter five numbers:");

        for (int i = 0; i < 5; i++) {
            numbers[i] = sc.nextInt();
            sum = sum + numbers[i];
        }

        double average = sum / 5.0;

        System.out.println("Sum = " + sum);
        System.out.println("Average = " + average);

        sc.close();
    }
}


package org.example;

import java.util.Scanner;

public class App {
    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.print("Enter an alphabet: ");
        char ch = Character.toLowerCase(sc.next().charAt(0));

        if (ch < 'a' || ch > 'z') {
            System.out.println("Invalid input");
        }
        else if (ch == 'a' || ch == 'e' || ch == 'i'
                || ch == 'o' || ch == 'u') {
            System.out.println("Vowel");
        }
        else {
            System.out.println("Consonant");
        }

        sc.close();
    }
}



sudo apt update
sudo apt upgrade -y
sudo apt install software-properties-common -y
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install ansible -y
ansible --version



cd ~
mkdir Ansible_Experiment25
cd Ansible_Experiment25

ansible-galaxy init prerequisites
ansible-galaxy init postgresql
ansible-galaxy init apache

prerequisites/tasks/main.yml

---
- name: Update package cache
  apt:
    update_cache: yes

- name: Install Git
  apt:
    name: git
    state: present

postgresql/tasks/main.yml

---
- name: Install PostgreSQL
  apt:
    name: postgresql
    state: present

- name: Start and enable PostgreSQL
  service:
    name: postgresql
    state: started
    enabled: yes

apache/tasks/main.yml

---
- name: Install Apache web server
  apt:
    name: apache2
    state: present

- name: Start and enable Apache
  service:
    name: apache2
    state: started
    enabled: yes

stack.yml

---
- name: Configure server using Ansible roles
  hosts: localhost
  connection: local
  become: yes

  roles:
    - prerequisites
    - postgresql
    - apache
sudo ansible-playbook stack.yml
git --version
sudo systemctl status postgresql
sudo systemctl status apache2
dpkg -l git postgresql apache2



cd ~
mkdir Ansible_Experiment26
cd Ansible_Experiment26

nano application.yml

---
- name: Configure a simple web application
  hosts: localhost
  connection: local
  become: yes

  tasks:

    - name: Install Apache web server
      apt:
        name: apache2
        state: present
        update_cache: yes

    - name: Start and enable Apache service
      service:
        name: apache2
        state: started
        enabled: yes

    - name: Deploy HTML web page
      copy:
        content: |
          <html>
          <head>
              <title>My Web Application</title>
          </head>
          <body>
              <h1>Welcome to My Application</h1>
              <p>This application is deployed using Ansible.</p>
          </body>
          </html>
        dest: /var/www/html/index.html
        mode: '0644'

    - name: Verify application availability
      uri:
        url: http://localhost
        status_code: 200

    - name: Display success message
      debug:
        msg: "Web application is running successfully!"


sudo ansible-playbook application.yml
curl http://localhost


Common playbook 


---
- name: Configure web application using Ansible
  hosts: localhost
  connection: local
  become: yes

  tasks:
    - name: Install Apache
      apt:
        name: apache2
        state: present
        update_cache: yes

    - name: Start and enable Apache
      service:
        name: apache2
        state: started
        enabled: yes

    - name: Deploy HTML page
      copy:
        content: |
          <html>
          <head>
              <title>My Web Application</title>
          </head>
          <body>
              <h1>Welcome to My Web Application</h1>
              <p>Application deployed using Ansible.</p>
          </body>
          </html>
        dest: /var/www/html/index.html
        mode: '0644'

    - name: Verify HTTP response
      uri:
        url: http://localhost
        status_code: 200

    - name: Display success message
      debug:
        msg: "Application deployed successfully!"



commands 
sudo apt update
sudo apt install ansible -y
mkdir Ansible_Common
cd Ansible_Common
nano application.yml


sudo ansible-playbook application.yml

curl http://localhost

