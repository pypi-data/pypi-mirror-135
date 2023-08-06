[![tomnvt](https://circleci.com/gh/tomnvt/ios-debug.svg?style=shield&circle-token=ac247565d93c63e3e695882be5a5a3563c1553c5)](https://circleci.com/gh/tomnvt/ios-debug.svg?style=shield&circle-token=ac247565d93c63e3e695882be5a5a3563c1553c5)

# ios-debug

`ios-debug` is a tool for creating and managing mock implementation. It currently creates a mock implementation for each repository protocol within an iOS project.

## THREE THINGS...

...that the app is expected to have:

- there are repository protocols conforming to `...Repository` naming convention
- there is a single `rootViewController` assigned (doesn't matter in which file)
- there is a `ContainerBuilder.swift` file with `registerRepositoryLayer` function


## INSTALLATION

If you have some version of `pip`, either `pip install ios-debug` or `pip3 install ios-debug` should do the job.


## USAGE

There is a simple console UI that show when `ios-debug` is called. Names of the shown options should be pretty self-explanatory :-)

Each command can be also called by passing it as an argument to `ios-debug`, e.g. `ios-debug start` or `ios-debug stop`.


## WHEN IT STARTS

When the debug mode is starting, the following happens:

1. Swift files are gathered and read
2. Repository protocols are found
3. Protocols are parsed and function declarations are extracted
4. Repository mock implementation template is processed so there is a mock implementation for each protocol function for each repository. Also, `Container` registration are generated, overriding the origin registration.
5. Registration functions are added to `registerRepositoryLayer` function in `ContainerBuilder`.
6. `MockManager` and `ShakeableNavigationController` are generated.
    - `MockManager` enables user to choose different mock function implementations at runtime.
    - `ShakeableNavigationController` is used as `rootViewController`. It responds to shake gesterus by showing the `MockManager`.
7. `rootViewController` is reassigned to `ShakeableNavigationController`.
8. A Run Script build phase is added in order to sync* mock function variants and protocol functions during build.


## WHEN IT STOPS

When the debug mode is stopping, the following happens:
1. Swift files are gathered and read.
1. All mock repositories are gathered and saved to a binary file.
2. Calls to registration function are removed from `ContainerBuilder`.
3. `MockManager` and `ShakeableNavigationController` are removed and `ShakeableNavigationController` is unassigned as `rootViewController`.
4. The Run Script build phase is removed from the project.

*Syncing is basically just turning the debog mode off and on again. The whole process is designed to be a function of the code's state, so there are minimal side effect expectation during the processing.
