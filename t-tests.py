from scipy import stats

# Provided values
mean_response_area = 17.8
mean_response_line = 16.9
std_dev = 2.8
sample_size = 10

# Performing independent samples t-test
t_value, p_value = stats.ttest_ind_from_stats(mean1=mean_response_area, std1=std_dev, nobs1=sample_size,
                                              mean2=mean_response_line, std2=std_dev, nobs2=sample_size)

print("Calculated t-value:", t_value)
print("Resulting p-value:", p_value)
