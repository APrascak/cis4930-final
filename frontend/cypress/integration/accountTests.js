context('Actions', () => {
	beforeEach(() => {
		//cy.visit('http://localhost:3000/')
	})

    //#Integration
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
     
    //#Acceptance
    it('Should navigate to Account and create a Stock Account', () => {
        cy.visit('http://localhost:3000/home')
        cy.get('[name="navAccount"]').click()
        cy.contains('Create Stock Account').click()
        cy.get('[name="buySellStocksForm"]')
    })

     //#Integration
     it('Should make sure new account starts with zero of each stock', ()=>{
         cy.wait(20000)
         cy.get('h3').contains("PINS Stock Amount: 0, AXP Stock Amount: 0, UBER Stock Amount: 0, SNAP Amount: 0")
     })

    //#Integration
    it('Should be able to add sufficient funds to account', ()=>{
        cy.get('[name="inputFunds"]').type("500")
        cy.get('[name = "submitFunds"]').click()
    })

    //#Integration
    it('Should make sure user cannot sell stock that they do not own', () => {
        const stub = cy.stub()
        cy.on('window:alert', stub)

        cy.get('[name="action"]').select('Sell')
        cy.get('[name="stock"]').select('Pinterest Stock')
        cy.get('[name="submitStocks"]').click()

        cy.get('[name="sellError"]').contains('Invalid: you cannot sell stocks you do not own')  
    })

     //#Acceptance
     it('Should be able to buy stocks', ()=>{
         cy.get('[name="action"]').select('Buy')
         cy.get('[name="stock"]').select('Pinterest Stock')
         cy.get('[name="submitStocks"]').click()

         cy.get('[name="action"]').select('Buy')
         cy.get('[name="stock"]').select('American Express Stock')
         cy.get('[name="submitStocks"]').click()

        cy.get('[name="action"]').select('Buy')
        cy.get('[name="stock"]').select('Uber Stock')
         cy.get('[name="submitStocks"]').click()

         cy.get('[name="action"]').select('Buy')
         cy.get('[name="stock"]').select('Snapchat Stock')
         cy.get('[name="submitStocks"]').click()
         cy.wait(500)

         cy.wait(20000)

         cy.get('h3').contains("PINS Stock Amount: 1, AXP Stock Amount: 1, UBER Stock Amount: 1, SNAP Amount: 1")
     })
    
     //#Acceptance
     it('Should be able to sell a stock', ()=>{
         cy.get('[name="action"]').select('Sell')
         cy.get('[name="stock"]').select('American Express Stock')
        cy.get('[name="submitStocks"]').click()
         cy.get('h3').contains("PINS Stock Amount: 1, AXP Stock Amount: 0, UBER Stock Amount: 1, SNAP Amount: 1")
     })

    //#Integration
    it('Should not buy more stocks than has funds available', () =>{
        cy.get('[name="action"]').select('Buy')
        cy.get('[name="stock"]').select('American Express Stock')
        cy.get('[type="number"]').type('{backspace}')
        cy.get('[type="number"]').type('100')
        cy.get('[name="submitStocks"]').click()

        cy.get('[name="buyError"]').contains('Invalid: you do not have enough funds to buy these stocks')
    })
    
  
})
