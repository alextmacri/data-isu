import numpy as np
import statistics as stats
from enum import Enum
from question import Question

class OneVariableStatsQuestionType(Enum):
    ALL = 0
    MEAN = 1
    MEDIAN = 2
    MODES = 3
    RANGE = 4
    STDEV = 5

class OneVariableStatsQuestion(Question):
    def __init__(self, question_type, dataset_min: int=10, dataset_max: int=30, dataset_size: int=10, dataset_whole: bool=True) -> None:
        self.question_type = question_type
        dataset = self.generate_dataset(dataset_min, dataset_max, dataset_size, dataset_whole)

        self.prompt_base_key = {
            OneVariableStatsQuestionType.ALL: 'Find the mean, median, mode(s), range, and standard deviation of this dataset: %data%',
            OneVariableStatsQuestionType.MEAN: 'Find the mean of this dataset: %data%',
            OneVariableStatsQuestionType.MEDIAN: 'Find the median of this dataset: %data%',
            OneVariableStatsQuestionType.MODES: 'Find the mode(s) of this dataset: %data%',
            OneVariableStatsQuestionType.RANGE: 'Find the range of this dataset: %data%',
            OneVariableStatsQuestionType.STDEV: 'Find the standard deviation of this dataset: %data%',
        }

        self.answer_key = {
            OneVariableStatsQuestionType.MEAN: [round(stats.mean(dataset), 1)],
            OneVariableStatsQuestionType.MEDIAN: [round(stats.median(dataset), 1)],
            OneVariableStatsQuestionType.MODES: [x for x in stats.multimode(dataset)] if len(stats.multimode(dataset)) != len(dataset) else [],
            OneVariableStatsQuestionType.RANGE: [max(dataset) - min(dataset)],
            OneVariableStatsQuestionType.STDEV: [round(stats.stdev(dataset), 1)],
        }
        self.answer_key[OneVariableStatsQuestionType.ALL] = [*self.answer_key.values()]
        
        super().__init__(self.prompt_base_key[self.question_type], [dataset], self.answer_key[self.question_type])

    def generate_dataset(self, minimum: int, maximum: int, size: int, whole: bool) -> list[float]:
        if whole:
            dataset = [float(np.random.randint(minimum, maximum)) for _ in range(size)]
        else:
            dataset = [np.around(np.random.uniform(minimum, maximum), 1) for _ in range(size)]
        return dataset


if __name__ == '__main__':                              # Testing each type
    for q_type in list(OneVariableStatsQuestionType):
        q = OneVariableStatsQuestion(q_type)
        print(q.prompt, q.answer)