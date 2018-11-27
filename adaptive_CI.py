import numpy

MEAN = 4.0
STDDEV = 1.0
N = 2
MAX_N = 31
SHOW = 50
REPEAT = 1000
VERBOSE = False
INFINITY = 100000

#T = 2.13
T = {}
T[1] = 12.706; T[2] = 4.303; T[3] = 3.182; T[4] = 2.776; T[5] = 2.571
T[6] = 2.447; T[7] = 2.365; T[8] = 2.306; T[9] = 2.262; T[10] = 2.228
T[11] = 2.201; T[12] = 2.179; T[13] = 2.16; T[14] = 2.145; T[15] = 2.131
T[16] = 2.12; T[17] = 2.11; T[18] = 2.101; T[19] = 2.093; T[20] = 2.086
T[21] = 2.08; T[22] = 2.074; T[23] = 2.069; T[24] = 2.064; T[25] = 2.06
T[26] = 2.06; T[27] = 2.056; T[28] = 2.052; T[29] = 2.048; T[30] = 2.045
T[40] = 2.042
T[60] = 2.021
T[120] = 2.0
T[INFINITY] = 1.98

def calc_CI(samples):
	NUM_SAMPLES = len(samples)

	sample_mean = numpy.mean(samples)
	if VERBOSE:
		print("Sample mean:")
		print(sample_mean)

	diffs = [sample - sample_mean for sample in samples]
	if VERBOSE:
		print("Diffs:")
		print(diffs[:SHOW])
	
	unbiased_sample_std = numpy.sqrt(sum([diff*diff for diff in diffs])/float(NUM_SAMPLES-1))
	if VERBOSE:
		print("Unbiased sample std dev:")
		print(unbiased_sample_std)

	biased_sample_std = numpy.sqrt(sum([diff*diff for diff in diffs])/float(NUM_SAMPLES))
	if VERBOSE:
		print("Biased sample std dev:")
		print(biased_sample_std)

	CI = (sample_mean - T[NUM_SAMPLES-1] * unbiased_sample_std/numpy.sqrt(NUM_SAMPLES), sample_mean + T[NUM_SAMPLES-1] * unbiased_sample_std/numpy.sqrt(NUM_SAMPLES))

	return sample_mean, unbiased_sample_std, biased_sample_std, CI

def sample():
	samples = numpy.random.normal([MEAN for i in range(N)], [STDDEV for i in range(N)])
	if VERBOSE:
		print("Samples (through 50th):")
		print(samples[:SHOW])

	sample_mean, unbiased_sample_std, biased_std, CI = calc_CI(samples)
	return sample_mean, unbiased_sample_std, biased_std, CI

def adaptive_sample():
	samples = numpy.random.normal([MEAN for i in range(MAX_N)], [STDDEV for i in range(MAX_N)])
	unbiased_sample_std = None
	unbiased_std = None
	CI = (None, None)
	for i in range(2, MAX_N):
		current_samples = samples[:i]
		sample_mean, unbiased_sample_std, biased_std, CI = calc_CI(current_samples)
		#print(f"Current CI: {CI}")
		if abs(CI[1] - CI[0]) <= 2.0:
			break
	return sample_mean, unbiased_sample_std, biased_std, CI

def main():
	unbiased_ests = []
	biased_ests = []
	sample_means = []
	CIs = []
	for i in range(REPEAT):
		print(f"Starting repetition # {i}")
		#sample_mean, unbiased_est, biased_est, CI = sample()
		sample_mean, unbiased_est, biased_est, CI = adaptive_sample()
		unbiased_ests.append(unbiased_est)
		biased_ests.append(biased_est)
		sample_means.append(sample_mean)
		CIs.append(CI)

	CI_successes = 0
	for CI in CIs:
		if MEAN >= CI[0] and MEAN <= CI[1]:
			CI_successes += 1

	print("CIs:")
	print(CIs[:SHOW])

	print(f"True mean, STD DEV: {MEAN}, {STDDEV}")

	print("Unbiased estimates of std dev: ", numpy.mean(unbiased_ests))
	print("Biased estimates of std dev: ", numpy.mean(biased_ests))
	print("Sample mean estimate: ", numpy.mean(sample_means))
	print(f"# CI successes {CI_successes}")

if __name__ == "__main__":
	main()
