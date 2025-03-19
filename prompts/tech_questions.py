TECH_QUESTIONS = {
    "python": [
        "What are Python decorators and how do they work?",
        "Explain the difference between lists and tuples in Python.",
        "How do you handle exceptions in Python?",
        "Describe Python's Global Interpreter Lock (GIL) and its implications.",
        "What are context managers in Python and when would you use them?"
    ],
    "javascript": [
        "Explain the difference between '==' and '===' in JavaScript.",
        "What is closure in JavaScript and how does it work?",
        "Explain event delegation in JavaScript.",
        "What are Promises in JavaScript and how do they differ from callbacks?",
        "Describe the concept of hoisting in JavaScript."
    ],
    "java": [
        "What is the difference between an interface and an abstract class in Java?",
        "Explain the concept of Java Virtual Machine (JVM).",
        "What are the differences between HashMap and ConcurrentHashMap?",
        "How does garbage collection work in Java?",
        "Explain the concept of Java Streams and how they differ from collections."
    ],
    "react": [
        "What are React Hooks? Give examples of built-in hooks.",
        "Explain the concept of Virtual DOM in React.",
        "What is the difference between state and props in React components?",
        "How would you optimize performance in a React application?",
        "Explain the component lifecycle in React."
    ],
    "angular": [
        "What is dependency injection in Angular?",
        "Explain the difference between AngularJS and Angular 2+.",
        "What are Angular modules and how do they work?",
        "Explain the Angular component communication methods.",
        "What are Angular directives and their types?"
    ],
    "node.js": [
        "What is the event loop in Node.js?",
        "How does Node.js handle concurrency despite being single-threaded?",
        "What is middleware in Express.js?",
        "Explain the difference between process.nextTick() and setImmediate().",
        "How would you debug a Node.js application?"
    ],
    "sql": [
        "What's the difference between INNER JOIN and LEFT JOIN?",
        "Explain the concept of database normalization.",
        "What are stored procedures and what are their advantages?",
        "How would you optimize a slow SQL query?",
        "Explain the difference between HAVING and WHERE clauses."
    ],
    "mongodb": [
        "What are the key differences between MongoDB and relational databases?",
        "Explain sharding in MongoDB.",
        "What are MongoDB indexes and when would you use them?",
        "How does MongoDB handle transactions?",
        "Explain the concept of document validation in MongoDB."
    ],
    "docker": [
        "What is the difference between a Docker image and a container?",
        "Explain how Docker networking works.",
        "What is Docker Compose and when would you use it?",
        "How do you persist data in Docker containers?",
        "Explain the multi-stage build pattern in Docker."
    ],
    "aws": [
        "What is the difference between EC2 and Lambda?",
        "Explain the concept of IAM in AWS.",
        "What are the differences between S3 storage classes?",
        "How would you design a highly available architecture in AWS?",
        "Explain the concept of VPC in AWS."
    ],
    "cpp": [
        "What's the difference between stack and heap memory allocation?",
        "Explain polymorphism in C++.",
        "What are smart pointers and why are they used?",
        "Explain the Rule of Three/Five/Zero in C++.",
        "What's the difference between templates and macros in C++?"
    ],
    "django": [
        "Explain Django's MVT architecture.",
        "What are Django signals and when would you use them?",
        "How does Django's ORM work?",
        "Explain middleware in Django and give examples of its use.",
        "How would you optimize database queries in a Django application?"
    ],
    "flask": [
        "What is Flask's Application Context?",
        "How does Flask differ from Django?",
        "Explain Flask Blueprints and their advantages.",
        "How would you handle authentication in a Flask application?",
        "What are Flask extensions and name some common ones you've used."
    ],
    "devops": [
        "Explain the concept of Infrastructure as Code.",
        "What is CI/CD and how does it benefit development teams?",
        "How would you handle secrets in a CI/CD pipeline?",
        "Explain the concept of blue-green deployment.",
        "What monitoring tools have you used and how did you implement them?"
    ]
}

def get_tech_questions(tech):
    tech_lower = tech.lower()
    
    if tech_lower in TECH_QUESTIONS:
        return TECH_QUESTIONS[tech_lower]
    
    for key in TECH_QUESTIONS:
        if key in tech_lower or tech_lower in key:
            return TECH_QUESTIONS[key]
    
    return []