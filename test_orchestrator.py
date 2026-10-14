from orchestrator import Orchestrator

team = Orchestrator(provider="gemini")

idea = "Build a Student Management System where teachers can add, view, update, and delete student records."

print("\nStarting DevTeam AI...\n")

result = team.run(idea)

print("\n========== REQUIREMENTS ==========\n")
print(result["requirements"])

print("\n========== ARCHITECTURE ==========\n")
print(result["architecture"])

print("\nDevTeam AI workflow completed!")