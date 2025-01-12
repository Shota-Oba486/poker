import onnxruntime as ort
import numpy as np

# ONNXモデルのロード
class AI:
    def __init__(self):
        self.action_size = 6
        self.phases = ["preflop", "flop", "turn", "river"]
        self.pis = {}
        for phase in self.phases:
            self.pis[phase] = ort.InferenceSession("train/models/actor_critic/nonnormal/pi/onnx/"+phase+".onnx")

    def get_action(self, state,mask,phase_index):
        mask = np.array(mask)
        pi = self.pis[self.phases[phase_index]]
        state = np.array([state], dtype=np.float32)

        input_name = pi.get_inputs()[0].name
        output_name = pi.get_outputs()[0].name
        result = pi.run([output_name], {input_name: state})
        result = result[0][0]

        result = result * mask

        total = np.sum(result)
        probabilities = result / total

        # インデックスを確率に基づいてランダムに選択
        index = np.random.choice(len(result), p=probabilities)
        return index
    
if __name__ == "__main__":
    ai = AI()
    state = np.array([0,0,0,1,0,0,0,0.9,0.8,0.02,0,0.02,0,0,0,0,0])
    mask = [1,1,1,0,1,1]
    phase_index = 0

    ai.get_action(state,mask,phase_index)