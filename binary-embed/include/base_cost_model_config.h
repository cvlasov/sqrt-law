#ifndef BASE_COST_MODEL_CONFIG_H_
#define BASE_COST_MODEL_CONFIG_H_

class base_cost_model_config {
public:
	int payload_bits;
	bool verbose;
	int randSeed;

	base_cost_model_config(int payload_bits, bool verbose, int randSeed);
	~base_cost_model_config();
};

#endif
