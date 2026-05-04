import torch
from torch_geometric.nn import GraphSAGE
import torch.nn.functional as F

class MycorrhizalNetworkGNN(torch.nn.Module):
    def __init__(self, num_node_features, hidden_channels):
        super(MycorrhizalNetworkGNN, self).__init__()
        # GraphSAGE is optimal for inductive learning on large, evolving network topologies
        self.sage1 = GraphSAGE(num_node_features, hidden_channels, num_layers=2)
        self.sage2 = GraphSAGE(hidden_channels, int(hidden_channels/2), num_layers=2)
        self.classifier = torch.nn.Linear(int(hidden_channels/2), 1) # Output: Anomaly Score

    def forward(self, x, edge_index):
        # x: Node feature matrix [RZSM, carbon flux, dielectric anomaly, historical trend]
        # edge_index: Fungal connection matrix weighted by PHYSER correlation
        
        x = self.sage1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, p=0.2, training=self.training)
        
        x = self.sage2(x, edge_index)
        x = F.relu(x)
        
        anomaly_score = torch.sigmoid(self.classifier(x))
        return anomaly_score

if __name__ == "__main__":
    print("[*] Loading PyTorch Geometric GNN Architecture...")
    # 4 input features per tree root zone, 64 hidden channels
    model = MycorrhizalNetworkGNN(num_node_features=4, hidden_channels=64)
    print("[+] Architecture loaded and ready for localized RTX 3090 cluster training.")
