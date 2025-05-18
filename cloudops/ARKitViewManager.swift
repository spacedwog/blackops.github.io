@objc(ARKitViewManager)
class ARKitViewManager: RCTViewManager {
  override func view() -> UIView! {
    return ARKitView()
  }

  override static func requiresMainQueueSetup() -> Bool {
    return true
  }
}