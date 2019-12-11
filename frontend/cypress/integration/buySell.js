context('Actions', () => {
	beforeEach(() => {
		//cy.visit('http://localhost:3000/')
	})

	it('Should sign up new user and navigate to Account page', () => {
        let num = Math.round(Math.random() * 10000000)
        cy.visit('http://localhost:3000/signup')
		cy.get('input[name="username"]').type('test user')
        cy.get('input[name="email"]').type('test' + num + '@email.com')
        cy.get('input[name="passwordOne"]').type('longValidPassword')
        cy.get('input[name="passwordTwo"]').type('longValidPassword')
        cy.get('button').should('be.enabled')
		cy.get('form').submit()
		
		//Valid input should result in successful login to home panel
        cy.location('pathname').should('eq', '/home')
        
    })
     
    it('Should navigate to Account and create a Stock Account', () => {
        cy.visit('http://localhost:3000/home')
        cy.get('[name="navAccount"]').click()
        cy.contains('Create Stock Account').click()
        cy.get('[name="buySellStocksForm"]')
    })
    
    it('Should make sure new account starts with zero of each stock', ()=>{
        cy.get('h3').contains("PINS Stock Amount: 0, AXP Stock Amount: 0, UBER Stock Amount: 0, SNAP Amount: 0")
    })

    it('Should make sure user cannot sell stock that they do not own', () => {
        const stub = cy.stub()
        cy.on('window:alert', stub)

        cy.get('[name="action"]').select('Sell')
        cy.get('[name="stock"]').select('Pinterest Stock')
        cy.get('[type="number"]').type('1')
        cy.get('[name="buySellStocksForm"] > [type="submit"]').click()

        cy.get('[name="sellError"]').contains('Invalid: you cannot sell stocks you do not own')  
    })

    it('Should be able to buy stocks', ()=>{
        cy.get('[name="action"]').select('Buy')
        cy.get('[name="stock"]').select('Pinterest Stock')
        cy.get('[type="number"]').type('{backspace}')
        cy.get('[type="number"]').type('3')
        cy.get('[name="buySellStocksForm"] > [type="submit"]').click()

        cy.get('[name="action"]').select('Buy')
        cy.get('[name="stock"]').select('American Express Stock')
        cy.get('[type="number"]').type('{backspace}')
        cy.get('[type="number"]').type('3')
        cy.get('[name="buySellStocksForm"] > [type="submit"]').click()

        cy.get('[name="action"]').select('Buy')
        cy.get('[name="stock"]').select('Uber Stock')
        cy.get('[type="number"]').type('{backspace}')
        cy.get('[type="number"]').type('3')
        cy.get('[name="buySellStocksForm"] > [type="submit"]').click()

        cy.get('h3').contains("PINS Stock Amount: 3, AXP Stock Amount: 3, UBER Stock Amount: 3, SNAP Amount: 0")
    })
    
    it('Should be able to sell a stock', ()=>{
        cy.get('[name="action"]').select('Sell')
        cy.get('[name="stock"]').select('American Express Stock')
        cy.get('[type="number"]').type('{backspace}')
        cy.get('[type="number"]').type('1')
        cy.get('[name="buySellStocksForm"] > [type="submit"]').click()
        cy.get('h3').contains("PINS Stock Amount: 3, AXP Stock Amount: 2, UBER Stock Amount: 3, SNAP Amount: 0")
    })

    it('Should be able to sell all of a stock', ()=>{
        cy.get('[name="action"]').select('Sell')
        cy.get('[name="stock"]').select('Uber Stock')
        cy.get('[type="number"]').type('{backspace}')
        cy.get('[type="number"]').type('3')
        cy.get('[name="buySellStocksForm"] > [type="submit"]').click()
        cy.get('h3').contains("PINS Stock Amount: 3, AXP Stock Amount: 2, UBER Stock Amount: 0, SNAP Amount: 0")
    })
    
  
})
