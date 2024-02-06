const packageConfig = {
    'patterns': [
        "setup/**",
        "src/**",
        "!requirements.txt",
        "src/**",
        "!.serverless/**",
        "!venv/**",
        "!node_modules/**",
        "!.idea/**",
        "!node_modules**",
        "!package.json",
        "!package-lock.json",
        "!Pipfile",
        "!Pipfile.lock"
    ]
}

export default packageConfig;
