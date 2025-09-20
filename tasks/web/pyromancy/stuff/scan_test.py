import picklescan
import picklescan.scanner
import base64
import io

payload = "ls"
scan_result = picklescan.scanner.scan_pickle_bytes(io.BytesIO(base64.b64decode(payload)),None)

if scan_result.infected_files >= 1:
    print("Malware found")
else:
    print("Abobas")