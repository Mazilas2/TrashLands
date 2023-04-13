module.exports = {
    publishers: [
      {
        name: '@electron-forge/publisher-github',
        config: {
          repository: {
            owner: 'Mazilas2',
            name: 'TrashLands',
          },
          prerelease: false,
          draft: true,
        },
      },
    ],
  }