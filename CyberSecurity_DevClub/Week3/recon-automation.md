# Automation & Scripting for Reconnaissance

## Why Automate Reconnaissance?

**The Scale Problem**
Manual reconnaissance works for single targets, but modern security assessments often involve:
- **Hundreds of subdomains** per organization
- **Multiple target organizations** in large engagements  
- **Continuous monitoring** for changes over time
- **Consistent methodology** across different team members

**The Human Error Factor**
Manual processes are prone to:
- **Missed targets**: Forgetting to check certain services or ports
- **Inconsistent coverage**: Different testers checking different things
- **Documentation gaps**: Forgetting to record important findings
- **Fatigue errors**: Making mistakes during long reconnaissance sessions

**The Time Reality**
What takes hours manually can be done in minutes with automation:
- **Subdomain discovery**: 30+ minutes manual vs 2 minutes automated
- **Port scanning**: Hours for full scans vs minutes with proper parallelization
- **Report generation**: Manual compilation vs automatic formatting

---

## Building Your First Reconnaissance Script

### The Philosophy of Good Automation

Think of reconnaissance automation like building an assembly line. Each station has a specific purpose:

1. **Input Validation Station**: Check that you have valid targets
2. **Collection Station**: Gather raw data from multiple sources
3. **Processing Station**: Clean and organize the data
4. **Analysis Station**: Find patterns and correlate information
5. **Output Station**: Generate actionable reports

### Essential Script Components

**Input Validation - Always Start Here**
```bash
# Check if target is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <target>"
    exit 1
fi

# Check if required tools are installed
command -v subfinder >/dev/null || { echo "subfinder not found"; exit 1; }
```

**Directory Organization - Keep Things Tidy**
```bash
# Create timestamped output directory
OUTDIR="${TARGET}_recon_$(date +%Y%m%d_%H%M%S)"
mkdir -p $OUTDIR/{dns,subdomains,ports,reports}
```

**Progress Reporting - Keep Users Informed**
```bash
echo "[+] Starting Phase 1: Domain Intelligence"
echo "   - Collecting WHOIS data..."
echo "   - Found $(wc -l < results.txt) results"
```

### Advanced Automation Concepts

**Parallel Processing - The Speed Multiplier**
The biggest performance gain in reconnaissance comes from running multiple operations simultaneously. Most reconnaissance tasks are I/O bound (waiting for network responses), so running them in parallel dramatically reduces total time.

**Key Concepts:**
- **Background processes**: Use `&` to run commands in background
- **Process synchronization**: Use `wait` to ensure all background jobs complete
- **Resource limits**: Don't overwhelm your system or the target

```bash
# Basic parallel execution
{
    subfinder -d $TARGET -silent > subdomains1.txt &
    amass enum -passive -d $TARGET > subdomains2.txt &
    wait  # Wait for both to complete
}
```

**Error Handling - Making Scripts Bulletproof**
Real-world scripts must handle failures gracefully. Networks are unreliable, tools crash, and targets may be unresponsive.

**Essential Error Handling Patterns:**
- **Tool availability checks**: Verify tools are installed before running
- **Timeout handling**: Don't let scripts hang indefinitely
- **Graceful degradation**: Continue with available tools if some fail
- **Logging**: Track what worked and what didn't

```bash
# Tool checking example
check_tool() {
    if ! command -v $1 &> /dev/null; then
        echo "Error: $1 not installed"
        return 1
    fi
}
```

**Data Management - Organizing Your Intelligence**
Good automation isn't just about collecting data - it's about organizing it for analysis. Structure your output so findings are easy to review and correlate.

**Best Practices:**
- **Consistent naming**: Use timestamps and target names
- **Hierarchical directories**: Separate different types of data
- **Standardized formats**: Use CSV, JSON for machine-readable output
- **Summary reports**: Provide human-readable overviews

---

## Python vs Bash for Reconnaissance

### When to Use Bash
Bash excels for:
- **Simple tool orchestration**: Chaining existing tools together
- **File system operations**: Creating directories, moving files
- **Text processing**: grep, sed, awk for parsing output
- **Rapid prototyping**: Quick scripts for immediate needs

### When to Use Python
Python is better for:
- **Complex data processing**: Parsing JSON, correlating information
- **API interactions**: REST APIs, web scraping
- **Error handling**: More sophisticated exception handling
- **Data analysis**: Statistical analysis, pattern recognition

### Building Your Reconnaissance Toolkit

**Start Simple - The 80/20 Rule**
80% of your reconnaissance needs can be met with simple scripts that:
1. **Validate input** (target domain provided?)
2. **Run 2-3 core tools** (subfinder, httpx, nmap)
3. **Organize output** (separate directories for different data types)
4. **Generate summary** (what was found?)

**Script Evolution Process:**
1. **Manual workflow**: Do it by hand first
2. **Basic automation**: Script the repetitive parts
3. **Add error handling**: Make it robust
4. **Optimize performance**: Add parallelization
5. **Enhance output**: Better reporting and analysis

**Example Script Structure:**
```bash
#!/bin/bash
# Your script always follows this pattern:

# 1. Input validation
validate_input() { ... }

# 2. Tool availability
check_requirements() { ... }

# 3. Core reconnaissance
discover_subdomains() { ... }
scan_services() { ... }

# 4. Organize results
organize_output() { ... }

# 5. Generate report
create_summary() { ... }
```

---

## Building Reconnaissance Pipelines

**The Pipeline Concept**
Think of reconnaissance as a data pipeline where each stage processes and enriches the data:

1. **Target Input** → Domain names, IP ranges
2. **Discovery Stage** → Find subdomains, services
3. **Verification Stage** → Check what's actually live
4. **Analysis Stage** → Identify interesting targets
5. **Reporting Stage** → Present actionable findings

**Pipeline Benefits:**
- **Modularity**: Each stage can be improved independently
- **Reusability**: Stages can be used in different combinations
- **Debugging**: Easy to identify where problems occur
- **Scaling**: Can distribute stages across multiple systems

**Tool Integration Strategy:**
```bash
# Instead of running tools separately:
subfinder -d example.com > subs.txt
httpx -l subs.txt > live.txt
nuclei -l live.txt > vulns.txt

# Chain them together:
subfinder -d example.com -silent | httpx -silent | nuclei -t exposures/
```

---

## Writing Your Own Scripts

### Step 1: Define Your Workflow
Before writing any code, map out your manual process:
- What tools do you run?
- In what order?
- What do you do with the output?
- How do you know when you're done?

### Step 2: Start with a Simple Version
```bash
#!/bin/bash
# my_first_recon.sh

TARGET=$1
if [ -z "$TARGET" ]; then
    echo "Usage: $0 <domain>"
    exit 1
fi

echo "Starting recon for $TARGET"
subfinder -d $TARGET
echo "Recon complete"
```

### Step 3: Add Structure and Organization
- Create output directories
- Timestamp your results
- Separate different types of data
- Add progress indicators

### Step 4: Improve Robustness
- Check if tools are installed
- Handle missing or invalid input
- Add timeouts for long-running operations
- Log errors and successes

### Step 5: Optimize Performance
- Identify bottlenecks (usually network I/O)
- Run independent operations in parallel
- Cache results to avoid repeat work
- Monitor resource usage

### Common Scripting Patterns

**Configuration Management:**
```bash
# Use variables for easy modification
WORDLIST="/usr/share/wordlists/subdomains.txt"
TIMEOUT=300
MAX_THREADS=50
```

**Flexible Output:**
```bash
# Support different output formats
case $OUTPUT_FORMAT in
    "json") echo "$results" | jq '.' ;;
    "csv") echo "$results" | tr ' ' ',' ;;
    *) echo "$results" ;;
esac
```

**Tool Abstraction:**
```bash
# Wrap tools for consistent interface
discover_subdomains() {
    local domain=$1
    if command -v subfinder >/dev/null; then
        subfinder -d "$domain" -silent
    elif command -v amass >/dev/null; then
        amass enum -passive -d "$domain"
    else
        echo "No subdomain tools available" >&2
        return 1
    fi
}
```

---

## Learning Resources

**Essential Skills to Develop:**
- **Bash scripting fundamentals**: Variables, loops, functions, error handling
- **Command-line tools mastery**: Understanding tool options and output formats
- **Text processing**: grep, sed, awk for parsing and filtering
- **System administration**: File permissions, process management, logging

**Recommended Learning Path:**
1. **"The Linux Command Line"** by William Shotts - Master the foundation
2. **"Bash Cookbook"** by Carl Albing - Learn practical scripting patterns
3. **"Automate the Boring Stuff with Python"** by Al Sweigart - Python automation basics

**Online Resources:**
- **Bash Academy**: https://guide.bash.academy/ (comprehensive bash guide)
- **ExplainShell**: https://explainshell.com/ (understand complex command lines)
- **ShellCheck**: https://www.shellcheck.net/ (validate your bash scripts)

**Practice Projects:**
1. **Log analyzer**: Parse web server logs for reconnaissance indicators
2. **Domain monitor**: Track changes in an organization's DNS records
3. **Report generator**: Convert tool output into professional reports
4. **Continuous scanner**: Monitor multiple targets for new services

---

## Best Practices for Reconnaissance Automation

### Design Principles
- **Single responsibility**: Each script should do one thing well
- **Composability**: Scripts should work together via pipes and files
- **Configurability**: Use variables and config files, not hard-coded values
- **Documentation**: Include usage examples and explain complex logic

### Operational Security
- **Rate limiting**: Don't overwhelm targets with requests
- **Stealth considerations**: Spread scans over time, use multiple source IPs
- **Legal compliance**: Only scan targets you have permission to test
- **Data protection**: Secure storage of reconnaissance results

### Performance and Reliability
- **Resource monitoring**: Track CPU, memory, and network usage
- **Graceful degradation**: Continue working when some tools fail
- **Result validation**: Verify output makes sense before proceeding
- **Backup strategies**: Don't lose hours of reconnaissance work

---

## Quick Start Guide

### Your First 30 Minutes
1. **Pick a simple workflow**: Subdomain discovery for a domain you own
2. **Write basic script**: Input validation + one tool + output organization
3. **Test and iterate**: Run it, fix problems, add features
4. **Add one enhancement**: Parallel execution or better error handling

### Building Your Toolkit
Start with these essential scripts:
- **Domain intelligence gatherer**: WHOIS, DNS records, certificate data
- **Subdomain discovery pipeline**: Multiple tools working together
- **Service scanner**: Port scanning with service identification
- **Report generator**: Convert raw data into readable summaries

### Advanced Projects
Once comfortable with basics:
- **Continuous monitoring system**: Track changes over time
- **Multi-target orchestrator**: Manage reconnaissance across many targets
- **Intelligence correlator**: Find relationships between different data sources
- **Custom tool integration**: Incorporate proprietary or specialized tools

Remember: Good automation doesn't replace thinking - it amplifies it. Start simple, focus on reliability over complexity, and always understand what your scripts are actually doing!