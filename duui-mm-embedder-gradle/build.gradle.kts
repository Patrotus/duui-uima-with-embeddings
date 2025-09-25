plugins {
    java
}

group = "org.texttechnology"
version = "1.0-SNAPSHOT"

dependencies {
    implementation("com.github.texttechnologylab:UIMATypeSystem:Tag")
    implementation("com.github.texttechnologylab:DockerUnifiedUIMAInterface:1.5.3")

    testImplementation("org.junit.jupiter:junit-jupiter:5.9.0")
    testImplementation("org.dkpro.core:dkpro-core-api-segmentation-asl:2.4.0")
    testImplementation("org.dkpro.core:dkpro-core-io-xmi-asl:2.4.0")
    testImplementation("org.dkpro.core:dkpro-core-io-json-asl:2.0.0")
    testImplementation("org.dkpro.core:dkpro-core-api-resources-asl:2.4.0")
    testImplementation("org.junit.platform:junit-platform-engine:1.9.0")
    testImplementation("org.junit.platform:junit-platform-launcher:1.9.0")
}

java {
    sourceCompatibility = JavaVersion.VERSION_21
    targetCompatibility = JavaVersion.VERSION_21
}

tasks.withType<Test> {
    useJUnitPlatform()
    testLogging {
        events("passed", "skipped", "failed")
    }
}

tasks.withType<JavaCompile> {
    options.encoding = "UTF-8"
}

sourceSets {
    test {
        java {
            srcDir("src/test/java")
        }
    }
}