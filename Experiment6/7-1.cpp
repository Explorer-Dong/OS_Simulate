#include <bits/stdc++.h>
#include <pthread.h>
#include <ctype.h>
#include <semaphore.h>
using i64 = unsigned long long int;

auto get_current_time()
{
    auto now = std::chrono::system_clock::now();
    auto timestamp = std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()).count();
    return timestamp;
};

auto start_time = get_current_time();

sem_t mutex;
int total_words = 0;
void* count_words(void* arg)
{
	std::vector<i64> time_vec;
	char* filename = (char*)arg;
	FILE *fp;
	int c, prevc = '\0';
	if ((fp = fopen(filename, "r")) != NULL)
	{
		while ((c = getc(fp)) != EOF)
		{
			if (!isalnum(c) && isalnum(prevc))
			{
				sem_wait(&mutex);
				auto cur = get_current_time();
				time_vec.push_back(cur - start_time);
				total_words++;
				std::this_thread::sleep_for(std::chrono::milliseconds(100));
				sem_post(&mutex);
			}
			else std::this_thread::sleep_for(std::chrono::milliseconds(100));
			prevc = c;
		}
		if (isalnum(prevc))
		{
			sem_wait(&mutex);
			auto cur = get_current_time();
			time_vec.push_back(cur - start_time);
			total_words++;
			sem_post(&mutex);
		}
		fclose(fp);
	}
	else
		perror(filename);
		
	printf("File[%s]: ", filename);
	for (auto time: time_vec)
		printf("%lld ", time);
	printf("\n");
	
	return nullptr;
}

int main(int ac, char *av[])
{
	if (ac != 3)
	{
		printf("Usage:%s file1 file2\n", av[0]);
		return 1;
	}
	sem_init(&mutex, 0, 1);
	pthread_t t1, t2;
	pthread_create(&t1, nullptr, count_words, av[1]);
	pthread_create(&t2, nullptr, count_words, av[2]);
	pthread_join(t1, nullptr);
	pthread_join(t2, nullptr);
	printf("Total words: %d\n", total_words);
	sem_destroy(&mutex);
	return 0;
}