#!/bin/sh

echo "TYPE:IMPACT"
echo "VULN:$CVE"
echo "PERCENTAGE:100"
echo "AFFECTED_PRODUCT:$BASENAME"
echo "VULNERABLE_PRODUCT:$LOG4J_FILE"
echo "ANALYSIS:Log4J Jar found on host at [$1] is vulnerable to $CVE"
echo "RECOMMENDATION:Upgrade to latest version of Log4J Jar"
