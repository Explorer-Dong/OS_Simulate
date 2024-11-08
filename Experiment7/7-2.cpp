#include <bits/stdc++.h>
#include <pthread.h>
#include <ctype.h>
#include <semaphore.h>
using i64 = unsigned long long int;

struct buf
{
	char* filename;
	int wc_count;
}args[2];


auto get_current_time()
{
    auto now = std::chrono::system_clock::now();
    auto timestamp = std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()).count();
    return timestamp;
};

auto start_time = get_current_time();

void* count_words(void* arg)
{
	std::vector<i64> time_vec;
	buf* ptr = (buf*)arg;
	char* filename = ptr->filename;
	FILE *fp;
	int c, prevc = '\0';
	if ((fp = fopen(filename, "r")) != NULL)
	{
		while ((c = getc(fp)) != EOF)
		{
			if (!isalnum(c) && isalnum(prevc))
			{
				auto cur = get_current_time();
				time_vec.push_back(cur - start_time);
				ptr->wc_count++;
			}
			prevc = c;
			std::this_thread::sleep_for(std::chrono::milliseconds(100));
		}
		if (isalnum(prevc))
		{
			auto cur = get_current_time();
			time_vec.push_back(cur - start_time);
			ptr->wc_count++;
		}
		fclose(fp);
	}
	else
		perror(filename);
	
	printf("File[%s]: ", filename);
	for (auto time: time_vec)
		printf("%lld ", time);
	printf("\n");
	
	pthread_exit((void*)&ptr->wc_count);
}

int main(int ac, char *av[])
{
	if (ac != 3)
	{
		printf("Usage:%s file1 file2\n", av[0]);
		return 1;
	}
	
	args[0] = {av[1], 0};
	args[1] = {av[2], 0};
	
	pthread_t t1, t2;
	
	if (pthread_create(&t1, nullptr, count_words, &args[0]) != 0)
	{
		perror("pthread_create");
		return 1;
	}
	if (pthread_create(&t2, nullptr, count_words, &args[1]) != 0)
	{
		perror("pthread_create");
		return 1;
	}
	void *result1, *result2;
	pthread_join(t1, &result1);
	pthread_join(t2, &result2);
	int total_words = *((int*)result1) + *((int*)result2);
	printf("Total words: %d\n", total_words);
	return 0;
}