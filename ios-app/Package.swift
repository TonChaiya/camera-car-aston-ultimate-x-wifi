// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "AstonCameraApp",
    platforms: [.iOS(.v17)],
    products: [
        .executable(name: "AstonCameraApp", targets: ["AstonCameraApp"])
    ],
    targets: [
        .executableTarget(
            name: "AstonCameraApp",
            path: "Sources/AstonCameraApp"
        ),
        .testTarget(
            name: "AstonCameraAppTests",
            dependencies: ["AstonCameraApp"],
            path: "Tests/AstonCameraAppTests"
        )
    ]
)
