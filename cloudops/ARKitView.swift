import Foundation
import ARKit
import SwiftUI

class ARKitView: UIView {
  override init(frame: CGRect) {
    super.init(frame: frame)
    let config = ARWorldTrackingConfiguration()
    let sceneView = ARSCNView(frame: self.bounds)
    sceneView.session.run(config)
    self.addSubview(sceneView)
  }

  required init?(coder: NSCoder) {
    fatalError("init(coder:) has not been implemented")
  }
}