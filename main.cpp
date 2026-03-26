#include <iostream>
#include <string>
#include <memory>
#include <vector>
#include <thread>
#include <chrono>
#include <csignal>
#include <atomic>

std::atomic<bool> keep_running(true);

void signal_handler(int signal) {
	keep_running = false;
}

// The Interface (Abstract Base Class)
// Defines what all telemetry types must be able to do
class TelemetryData {
public:
	virtual void process() = 0;
	virtual ~TelemetryData() {}
};

class GPSTelemetry : public TelemetryData {
public:
	void process() override {
		std::cout << "[GPS] Coordinates: 34.05N, 118.24W (Los Angeles)" << std::endl;
	}
};

class PowerTelemetry : public TelemetryData {
public:
	void process() override {
		std::cout << "[POWER] Battery: 88% | Voltage: 12.4V" << std::endl;
	}
};

class ThermalTelemetry : public TelemetryData {
public:
	void process() override {
		std::cout << "[THERMAL] Internal Temp: 42.5C | Status: NOMINAL" << std::endl;
	}
};

// The telemetry factory, which decides which object to create based on a string input
class TelemetryFactory {
public:
	static std::unique_ptr<TelemetryData> createPacket(std::string type) {
		if (type == "GPS") return std::make_unique<GPSTelemetry>();
		if (type == "POWER") return std::make_unique<PowerTelemetry>();
		if (type == "THERMAL") return std::make_unique<ThermalTelemetry>();
		return nullptr;
	}
};

int main() {
	std::signal(SIGINT, signal_handler);  // Listen for Ctrl+C

	while(keep_running) {
		// A list of the packet types we want to cycle through
		std::vector<std::string> types = {"GPS", "POWER", "THERMAL"};
		int index = 0;
	
		std::cout << "--- Satellite Stream Starting (Press Ctrl+C to stop) ---" << std::endl;
		
		while (true) {
			// Get the next type from our list
			std::string currentType = types[index % types.size()];
	
			// Use our Factory to create the packet
			auto packet = TelemetryFactory::createPacket(currentType);
	
			if (packet) {
				packet->process();
			}
	
			index++;
	
			std::this_thread::sleep_for(std::chrono::seconds(1));
		}
	}
	std::cout << "Satellite powering down safely..." << std::endl;
	return 0;
}