import asyncio
import json
from pathlib import Path

from analyzer.code_analyzer import CodeAnalyzer


async def main():
    # Initialize the analyzer
    analyzer = CodeAnalyzer()

    # Read the vulnerable application code
    vuln_app_path = Path('examples/vulnerable_app.py')
    with open(vuln_app_path, 'r') as f:
        content = f.read()

    print("Starting security analysis...")

    # Analyze the code
    report = await analyzer.analyze_code(content, str(vuln_app_path))

    # Calculate summary statistics
    report.calculate_summary()
    report.calculate_risk_score()

    # Print the results
    print("\nVulnerability Report:")
    print("=" * 80)
    print(f"File analyzed: {vuln_app_path}")
    print(f"Total vulnerabilities found: {report.summary['total']}")
    print(f"Risk score: {report.risk_score:.2f}")
    print("\nVulnerability distribution:")
    for severity, count in report.summary.items():
        if severity != 'total':
            print(f"  {severity}: {count}")

    print("\nDetailed vulnerabilities:")
    print("=" * 80)
    for vuln in report.vulnerabilities:
        print(f"\nType: {vuln.type}")
        print(f"Severity: {vuln.severity}")
        print(f"Location: {vuln.location.file_path}:{vuln.location.start_line}")
        print(f"Description: {vuln.description}")
        print(f"Impact: {vuln.impact}")
        print(f"Remediation: {vuln.remediation}")
        print("-" * 40)

    if report.chained_vulnerabilities:
        print("\nVulnerability Chains:")
        print("=" * 80)
        for chain in report.chained_vulnerabilities:
            print(f"\nChain Severity: {chain.combined_severity}")
            print(f"Attack Path: {chain.attack_path}")
            print("Vulnerabilities in chain:")
            for vuln in chain.vulnerabilities:
                print(f"  - {vuln.type} ({vuln.severity})")
            print("-" * 40)

    # Save the report to a file
    report_path = Path('vulnerability_report.json')
    with open(report_path, 'w') as f:
        json.dump(report.model_dump(), f, indent=2, default=str)
    print(f"\nDetailed report saved to {report_path}")

if __name__ == "__main__":
    asyncio.run(main())