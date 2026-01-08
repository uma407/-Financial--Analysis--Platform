"""
Standalone script to generate MD&A draft and save to file.
Usage: python generate_mda_output.py
"""
from src.mda_generator import MDAGenerator
from datetime import datetime

def main():
    print("Generating MD&A Draft...")
    generator = MDAGenerator()
    
    # Generate MD&A from sample data
    csv_path = "data/financial_statements.csv"
    draft = generator.generate_mda(csv_path)
    
    # Save to file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"MD&A_Draft_{timestamp}.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(draft)
    
    print(f"✅ MD&A Draft saved to: {filename}")
    print(f"📄 File size: {len(draft)} characters")
    return filename

if __name__ == "__main__":
    main()
