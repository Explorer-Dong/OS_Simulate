#include <bits/stdc++.h>
#include <pthread.h>
#include <ctype.h>
#include <semaphore.h>
using i64 = unsigned long long int;

std::ofstream fout("ans.out");
sem_t mutex_write;

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
		
	sem_wait(&mutex_write);
	
	fout << "File$$" << filename << "$$: ";
	for (auto time :time_vec) fout << time << " ";
	fout << "\n";
	
	sem_post(&mutex_write);
	
	return nullptr;
}

int main(int ac, char *av[])
{
	if (ac < 3)
	{
		printf("Usage:%s file1 file2\n", av[0]);
		return 1;
	}
	
	sem_init(&mutex, 0, 1);
	sem_init(&mutex_write, 0, 1);
	
	std::vector<pthread_t> t(ac);
	for (int i = 1; i < ac; i++)
	{
		pthread_create(&t[i], nullptr, count_words, av[i]);
	}
	
	for (int i = 1; i < ac; i++)
	{
		pthread_join(t[i], nullptr);
	}

	printf("Total words: %d\n", total_words);
	
	sem_destroy(&mutex_write);
	sem_destroy(&mutex);
	
	return 0;
}