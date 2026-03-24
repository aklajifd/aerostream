import unittest

def parse_telemetry_type(line):
    start = line.find("[") + 1
    end = line.find("]")
    return line[start:end] if start > 0 else "UNKNOWN"

class TestTelemetryProcessor(unittest.TestCase):
    def test_gps_parsing(self):
        sample = "[GPS] Lat: 34.05, Lon: -118.24"
        self.assertEqual(parse_telemetry_type(sample), "GPS")

    def test_thermal_parsing(self):
        sample = "[THERMAL] Temp: 42.5C"
        self.assertEqual(parse_telemetry_type(sample), "THERMAL")

if __name__ == '__main__':
    unittest.main()