#!/bin/sh

check_log4j_vuln()
{
	CVE="$1"
	shift
	VULN_VERSIONS="$*"
	LOG4J_FILES=`find / -name 'log4j-core-*.jar' -type f`
	for LOG4J_FILE in $LOG4J_FILES
	do
		for VULN_VERSION in $VULN_VERSIONS
		do
			BASENAME=`basename $LOG4J_FILE`
			LOG4J_VERSION=`echo $BASENAME | cut -c 12- | cut -c -6`
			if [ $LOG4J_VERSION = $VULN_VERSION ]; then
				echo "TYPE:IMPACT"
				echo "VULN:$CVE"
				echo "RATING:4"
				echo "PERCENTAGE:100"
				echo "AFFECTED_PRODUCT:$BASENAME"
				echo "VULNERABLE_PRODUCT:$LOG4J_FILE"
				echo "ANALYSIS:Log4J Jar found on host at [$LOG4J_FILE] is vulnerable to $CVE"
				echo "RECOMMENDATION:Upgrade to latest version of Log4J Jar"
				echo ""
			fi
		done
	done
}

CVE_2021_44228_LOG4J_VERSIONS="2.0-beta9 2.0-rc1 2.0-rc2 2.0.1 2.0.2 2.0 2.1 2.10.0 2.11.0 2.11.1 2.12.0 2.12.1 2.13.0 2.13.1 2.13.2 2.13.3 2.14.0 2.14.1"
check_log4j_vuln "CVE-2021-44228" $CVE_2021_44228_LOG4J_VERSIONS

CVE_2021_45046_LOG4J_VERSIONS="2.0-beta9 2.0-rc1 2.0-rc2 2.0.1 2.0.2 2.0 2.1 2.10.0 2.11.0 2.11.1 2.12.0 2.12.1 2.13.0 2.13.1 2.13.2 2.13.3 2.14.0 2.14.1 2.15.0"
check_log4j_vuln "CVE-2021-45046" $CVE_2021_45046_LOG4J_VERSIONS
