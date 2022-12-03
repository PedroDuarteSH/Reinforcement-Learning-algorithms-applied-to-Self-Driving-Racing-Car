import argparse
from model import Model

def main():
    args = process_arguments()
   
    model = Model(args)
    if(model.showResult and model.modelName != ""):
        model.showResults()
        
    model.createModel()
    model.createCallback()
    model.trainModel()
    model.saveModel()
    if(model.showResults):
        model.showResults()

def process_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--a", help="Algorithm To Be Used in Training", type=str, default="DQN", choices=["DQN", "A2C", "DDPG"])
    parser.add_argument("--ed", help="Enviroment Debug", type=bool, default=False)
    parser.add_argument("--s", help="Show Results, should be used with --d ant --m to specify the path of the model", type=bool, default=False)
    parser.add_argument("--m", help="Model Name", type=str, default="")
    parser.add_argument("--n", help="Use custom Network", type=bool, default=False)
    parser.add_argument("--t", help="Total Timesteps of training", type=int, default=1000000)
    parser.add_argument("--l", help="Log Interval", type=int, default=1)
    parser.add_argument("--p", help="Use Progress Bar In training", type=bool, default=True)
    parser.add_argument("--d", help="Directory to save model", type=str, default="final_models/")
    parser.add_argument("--v", help="Verbose", type=int, default=1)
    parser.add_argument("--b", help="Batch Size", type=int, default=64)
    parser.add_argument("--e", help="Exploration Fraction -> Used with DQN", type=float, default=0.1)
    parser.add_argument("--td", help="TensorFlow Log saving directory", type=str, default="traininglogs/")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()