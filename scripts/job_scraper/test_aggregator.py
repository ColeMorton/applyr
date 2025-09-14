#!/usr/bin/env python3
"""
Test script for the job descriptions aggregator.
"""

import sys
from datetime import datetime
from pathlib import Path

# Add the parent directory to the path so we can import the aggregator
sys.path.insert(0, str(Path(__file__).parent.parent))

from job_scraper.aggregate_jobs import JobDescriptionAggregator


def test_aggregator():
    """Test the job descriptions aggregator."""
    # Input and output paths
    input_dir = Path("data/outputs/job_descriptions")
    test_date = datetime.now().strftime('%Y%m%d')
    output_file = input_dir / f"{test_date}_test_aggregate.md"
    
    print("Testing job descriptions aggregator")
    print("Input directory: {input_dir}")
    print("Output file: {output_file}")
    print("=" * 50)
    
    # Initialize aggregator
    aggregator = JobDescriptionAggregator()
    
    # Run aggregation
    success = aggregator.aggregate_jobs(input_dir, output_file)
    
    if success:
        print("✅ Aggregation test successful!")
        
        # Display some stats about the generated file
        if output_file.exists():
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = len(content.split('\n'))
            chars = len(content)
            
            print("📄 Generated file stats:")
            print("   - Lines: {lines:,}")
            print("   - Characters: {chars:,}")
            print("   - Size: {chars/1024:.1f} KB")
            
            # Check for key sections
            sections_found = []
            if "## Summary Statistics" in content:
                sections_found.append("Summary Statistics")
            if "## Table of Contents" in content:
                sections_found.append("Table of Contents")
            if "## Job Descriptions" in content:
                sections_found.append("Job Descriptions")
            
            print("   - Sections found: {', '.join(sections_found)}")
        
    else:
        print("❌ Aggregation test failed!")
    
    return success

if __name__ == "__main__":
    success = test_aggregator()
    sys.exit(0 if success else 1)