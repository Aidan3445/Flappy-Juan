from FlappyJuan import FlappyJuan
from FlappyLearn import FlappyLearn
import argparse

parser = argparse.ArgumentParser(description="Flappy Juan")
parser.add_argument("-s", "--size", type=int, default=600, help="size of the game window")
parser.add_argument("-f", "--file-path", type=str, help=".txt file path for saving the best "
                                                        "performing neural net weights")

modes = parser.add_subparsers(title="modes", dest="learn")
learn = modes.add_parser(name="learn")
learn.add_argument("pop", type=int, help="size of the population for each training generation.")
learn.add_argument("-c", "--cont", action="store_true", help="continue training with a population from the "
                                                             "saved best performing neural net weights.")
learn.add_argument("-mr", "--mutation-rate", type=float, help="mutation rate for neuro-evolution (default: 0.25).")
learn.add_argument("-ma", "--mutation-amount", type=float, help="mutation amount for neuro-evolution. (default: 0.1).")


if __name__ == "__main__":
    args = parser.parse_args()
    file = args.file_path
    if args.learn:
        popSize = args.pop
        mutateRate = args.mutation_rate
        mutateAmount = args.mutation_amount
        cont = args.cont
        fj = FlappyLearn(600, popSize, fileName=file, mutateRate=mutateRate, mutateAmount=mutateAmount, cont=cont)
    else:
        fj = FlappyJuan(600, fileName=file)
    fj.play()
